"""Functions for interacting with Jira issues via the API."""

from typing import Optional
from .general import jira_api_request, get_priorities


def get_issue_creation_metadata(
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
    if new_priority not in get_priorities():
        return {
            "successful": False,
            "status_code": 406,
            "text": "Not supported priority. Use get_priorities() to get the allowed priorities.",
            "reason": "Priority was checked against get_priorities() and it was not part of them.",
        }

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


def change_issue_parent(issue_key: str, parent: str):
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    # TODO: This returns "Success 204" with different variations however the parent is not set.

    payload = {
        "update": {
            "parent": [
                {
                    "set": {"key": parent},
                }
            ]
        }
    }

    return jira_api_request(
        method="PUT",
        endpoint=f"issue/{issue_key}",
        headers=headers,
        payload=payload,
    )


def link_issues():
    # TODO: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-links/#api-rest-api-3-issuelink-post
    return None


def get_issue_link_types():
    # TODO: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-link-types/#api-rest-api-3-issuelinktype-get
    return None


def delete_issues_link():
    # TODO: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-links/#api-rest-api-3-issuelink-linkid-delete
    return None


def delete_issue(issue_key: str) -> dict:
    """
    Delete a Jira issue by its key.

    :param issue_key: Key of the Jira issue to delete.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    return jira_api_request(
        method="DELETE",
        endpoint=f"issue/{issue_key}",
    )


def assign_issue(issue_key: str, user: dict) -> dict:
    """
    Assign a Jira issue to a user.

    :param issue_key: Key of the Jira issue to assign.
    :param user: Dictionary containing the user information to assign to the issue.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    return jira_api_request(
        method="PUT",
        endpoint=f"issue/{issue_key}/assignee",
        headers=headers,
        payload=user,
    )


def comment_issue(issue_key: str, comment: str) -> dict:
    """
    Add a comment to a Jira issue.

    :param issue_key: Key of the Jira issue to comment on.
    :param comment: The text of the comment to add.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    payload = {
        "body": {
            "content": [
                {
                    "content": [
                        {
                            "text": comment,
                            "type": "text"
                        }
                    ],
                    "type": "paragraph"
                }
            ],
            "type": "doc",
            "version": 1,
        }
    }

    return jira_api_request(
        method="POST",
        endpoint=f"issue/{issue_key}/comment",
        headers=headers,
        payload=payload,
    )
