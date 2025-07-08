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
) -> dict:
    """
    Make a request to the Jira API with the specified method, endpoint, and
    optional parameters or payload.

    :param method: HTTP method to use (e.g., 'GET', 'POST').
    :param endpoint: API endpoint to call.
    :param headers: Optional HTTP headers to include in the request.
    :param params: Query parameters to include in the request.
    :param payload: Data to send in the body of the request.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
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
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {
                "successful": response.ok,
                "status_code": response.status_code,
                "text": response.text,
                "reason": response.reason,
            }
    else:
        return {
            "successful": response.ok,
            "status_code": response.status_code,
            "text": response.text,
            "reason": response.reason,
        }


def get_projects() -> dict:
    """
    Get all projects from Jira.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    return jira_api_request(
        method="GET",
        endpoint="project",
    )


def get_project_users(project_keys: str) -> dict:
    """
    Get all users associated with a given Jira project.

    :param project_key: Key of the Jira project.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """

    query_params = {"projectKeys": project_keys}

    return jira_api_request(
        method="GET",
        endpoint="user/assignable/multiProjectSearch",
        params=query_params,
    )


def get_project_issues(project_key: str) -> dict:
    """
    Get all issues for a given project from Jira.

    :param project_key: Key of the Jira project

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """

    query_params = {"currentProjectId": project_key}

    return jira_api_request(
        method="GET",
        endpoint="issue/picker",
        params=query_params,
    )


def get_priorities() -> dict:
    """
    Returns the list of all usable issue priorities.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    return jira_api_request(
        method="GET",
        endpoint="priority",
    )


def get_labels(max_results: int = 50) -> dict:
    """
    Retrieve all labels available in Jira.

    :param max_results: Maximum number of labels to return.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    query_params = {"maxResults": max_results}

    return jira_api_request(
        method="GET",
        endpoint="label",
        params=query_params,
    )


def get_project_issue_types(project_key: str, max_results: int = 50) -> dict:
    """
    Retrieve all issue types available for a specific Jira project.

    :param project_key: Key of the Jira project.
    :param max_results: Maximum number of issue types to return.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    query_params = {"maxResults": max_results}

    return jira_api_request(
        method="GET",
        endpoint=f"issue/createmeta/{project_key}/issuetypes",
        params=query_params,
    )


def get_issue_metadata(  # TODO: Rename?
    project_key: str,
    issue_type_id: str,
    max_results: int = 100
) -> dict:
    """
    Retrieve issue creation metadata for a specific project and issue type.

    :param project_key: Key of the Jira project.
    :param issue_type_id: ID of the issue type.
    :param max_results: Maximum number of fields to return.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """

    query_params = {"maxResults": max_results}

    return jira_api_request(
        method="GET",
        endpoint=f"issue/createmeta/{project_key}/issuetypes/{issue_type_id}",
        params=query_params,
    )


def get_current_user() -> dict:
    """
    Retrieve information about the currently authenticated Jira user.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    return jira_api_request(
        method="GET",
        endpoint="myself",
    )


def get_issue_fields() -> dict:
    """
    Retrieve all available fields that an issue can contain in the Jira instance.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    return jira_api_request(
        method="GET",
        endpoint="field",
    )


def get_issue_statuses() -> dict:
    """
    Retrieve all issue statuses defined in the Jira instance.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    return jira_api_request(
        method="GET",
        endpoint="status",
    )


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
) -> dict:
    # TODO: Add sprint, which?
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

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
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


def edit_issue(
    issue_key: str,
    value_key: str,
    value_to_update: object,
    action: Optional[str] = None,
) -> dict:
    """
    Edit a field of a Jira issue with a specified value and action.

    :param issue_key: Key of the Jira issue to update.
    :param value_key: Field key to update (e.g., 'summary', 'labels').
    :param value_to_update: Value to set or update for the field.
    :param action: Action to perform (e.g., 'set', 'add', 'remove'). 
                   If None, value_to_update is used directly.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    payload = {
        "update": {
            value_key: (
                [
                    {
                        action: value_to_update,
                    }
                ]
                if action
                else value_to_update
            )
        }
    }

    return jira_api_request(
        method="PUT",
        endpoint=f"issue/{issue_key}",
        headers=headers,
        payload=payload,
    )


def change_issue_title(issue_key: str, new_title: str) -> dict:
    """
    Change the summary/title of a Jira issue.

    :param issue_key: Key of the Jira issue to update.
    :param new_title: New summary/title for the issue.
    
    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    return edit_issue(
        issue_key=issue_key,
        value_key="summary",
        value_to_update=new_title,
        action="set",
    )


def change_issue_description(issue_key: str, new_description: str) -> dict:
    """
    Change the description of a Jira issue.

    :param issue_key: Key of the Jira issue to update.
    :param new_description: New description for the issue.
    
    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    payload = {
        "content": [
            {
                "content": [
                    {
                        "text": new_description,
                        "type": "text",
                    }
                ],
                "type": "paragraph",
            }
        ],
        "type": "doc",
        "version": 1,
    }

    return edit_issue(
        issue_key=issue_key,
        value_key="description",
        value_to_update=payload,
        action="set",
    )


def change_issue_reporter(issue_key: str, user: dict) -> dict:
    """
    Change the reporter of a Jira issue.

    :param issue_key: Key of the Jira issue to update.
    :param user: Dictionary (as returned by get_project_users()) containing the new reporter's 
                 information. Always get the user's information first from get_project_users().

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    return edit_issue(
        issue_key=issue_key,
        value_key="reporter",
        value_to_update=user,
        action="set",
    )


def change_issue_priority(issue_key: str, new_priority: dict) -> dict:
    """
    Change the priority of a Jira issue.

    :param issue_key: Key of the Jira issue to update.
    :param new_priority: Dictionary (as returned by get_priorities()) containing the new priority 
                         information. Always get the available priorities from get_priorities().

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    # TODO: check whether provided priority fits allowed priorities using get_priorities
    return edit_issue(
        issue_key=issue_key,
        value_key="priority",
        value_to_update=new_priority,
        action="set",
    )


def change_issue_environment(issue_key: str, new_environment: str) -> dict:
    """
    Change the environment field of a Jira issue.

    :param issue_key: Key of the Jira issue to update.
    :param new_environment: New environment description for the issue.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    payload = {
        "content": [
            {
                "content": [
                    {
                        "text": new_environment,
                        "type": "text",
                    }
                ],
                "type": "paragraph",
            }
        ],
        "type": "doc",
        "version": 1,
    }

    return edit_issue(
        issue_key=issue_key,
        value_key="environment",
        value_to_update=payload,
        action="set",
    )


def add_issue_labels(issue_key: str, new_labels: list[str]) -> dict:
    """
    Add one or more labels to a Jira issue.

    :param issue_key: Key of the Jira issue to update.
    :param new_labels: List of labels to add to the issue.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    labels = [{"add": label} for label in new_labels]
    return edit_issue(
        issue_key=issue_key,
        value_key="labels",
        value_to_update=labels,
    )


def change_issue_labels(issue_key: str, new_labels: list[str]) -> dict:
    """
    Replace all labels of a Jira issue with a new set of labels.

    :param issue_key: Key of the Jira issue to update.
    :param new_labels: List of new labels to set for the issue.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    return edit_issue(
        issue_key=issue_key,
        value_key="labels",
        value_to_update=new_labels,
        action="set",
    )

def delete_issue(issue_key: str):
    # TODO: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-issueidorkey-delete

def remove_issue_labels(issue_key: str, labels: list[str]) -> dict:
    """
    Remove one or more labels from a Jira issue.

    :param issue_key: Key of the Jira issue to update.
    :param labels: List of labels to remove from the issue.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    labels = [{"remove": label} for label in labels]
    return edit_issue(
        issue_key=issue_key,
        value_key="labels",
        value_to_update=labels,
    )


def update_issue_duedate(issue_key: str, new_duedate: str) -> dict:
    """
    Update the due date of a Jira issue.

    :param issue_key: Key of the Jira issue to update.
    :param new_duedate: New due date for the issue in 'YYYY-MM-DD' format.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    return edit_issue(
        issue_key=issue_key,
        value_key="duedate",
        value_to_update=new_duedate,
        action="set",
    )


    return None


def assign_issue(issue_key: str, user_id: str):
    # TODO: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-issueidorkey-assignee-put
    return None


def comment_issue(issue_key: str):
    # TODO: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-comments/#api-rest-api-3-issue-issueidorkey-comment-post
    return None
