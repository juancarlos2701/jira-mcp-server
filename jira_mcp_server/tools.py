"""
Utility functions for interacting with the Jira API.
"""

import os
from urllib.parse import urljoin
from typing import Optional
import requests
from requests.auth import HTTPBasicAuth

JIRA_AUTH = HTTPBasicAuth(str(os.getenv("JIRA_USER")), str(os.getenv("JIRA_API_KEY")))


def jira_api_request(
    method: str,
    endpoint: str,
    headers: Optional[dict] = None,
    params: Optional[dict] = None,
    payload: Optional[dict] = None,
):
    """
    Make a request to the Jira API with the specified method, endpoint, and
    optional parameters or payload.

    :param method: HTTP method to use (e.g., 'GET', 'POST').
    :param endpoint: API endpoint to call.
    :param params: Query parameters to include in the request.
    :param payload: Data to send in the body of the request.
    """

    endpoint = urljoin(str(os.getenv("JIRA_BASE_URL")), endpoint)

    headers = headers or {"Accept": "application/json"}

    response = requests.request(
        method=method,
        url=endpoint,
        headers=headers,
        params=params,
        json=payload,
        auth=JIRA_AUTH,
        timeout=int(os.getenv("REQUESTS_TIMEOUT")),
    )

    if response.ok:
        return response.json()
    else:
        return {
            "status_code": response.status_code,
            "text": response.text,
            "reason": response.reason,
        }


def get_projects():
    """
    Get all projects from Jira.
    """
    return jira_api_request(
        method="GET",
        endpoint="project",
    )


def get_project_users(project_keys: str):
    """
    Get all users associated with a given Jira project.

    :param project_key: Key of the Jira project.
    """

    query_params = {"projectKeys": project_keys}

    return jira_api_request(
        method="GET",
        endpoint="user/assignable/multiProjectSearch",
        params=query_params,
    )


def get_project_issues(project_key: str):
    """
    Get all issues for a given project from Jira.

    :param project_key: Key of the Jira project
    """

    query_params = {"currentProjectId": project_key}

    return jira_api_request(
        method="GET",
        endpoint="issue/picker",
        params=query_params,
    )


def get_priorities():
    """
    Returns the list of all issue priorities.
    """
    return jira_api_request(
        method="GET",
        endpoint="priority",
    )


def update_issue(issue_key: str, title: str, description: str):
    """
    Update an existing Jira issue with the specified parameters.
    """
    # TODO
    return None


def create_issue(
    project_key: str,
    title: str,
    description: str,
    issuetype: str,
    duedate: Optional[str] = None,
    assignee_id: Optional[str] = None,
    labels: Optional[list[str]] = None,
    priority_id: Optional[str] = None,
    reporter_id: Optional[str] = None,
) -> requests.Response:
    """
    Create a new Jira issue with the specified parameters.

    :param project_key: Key of the Jira project.
    :param title: Summary/title of the issue.
    :param description: Detailed description of the issue.
    :param issuetype: Type of the issue (e.g., Task, Bug).
    :param duedate: Due date for the issue (optional). Shall be in format "YYYY-MM-dd"
    :param assignee_id: ID of the assignee (optional).
    :param labels: List of labels to add to the issue (optional).
    :param priority_id: ID of the priority of the issue (optional).
    :param reporter_id: ID of the reporter of the issue (optional).
    """
    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": title,
            "issuetype": {"name": issuetype},
            "description": {
                "content": [
                    {
                        "content": [
                            {
                                "text": description,
                                "type": "text",
                            }
                        ],
                        "type": "paragraph",
                    }
                ],
                "type": "doc",
                "version": 1,
            },
        }
    }

    if duedate:
        payload["fields"].update({"duedate": duedate})
    if assignee_id:
        payload["fields"].update({"assignee": {"id": assignee_id}})
    if labels:
        payload["fields"].update({"labels": labels})
    if priority_id:
        payload["fields"].update({"priority": {"id": priority_id}})
    if reporter_id:
        payload["fields"].update({"reporter": {"id": reporter_id}})

    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    return jira_api_request(
        method="POST",
        endpoint="issue",
        headers=headers,
        payload=payload,
    )
