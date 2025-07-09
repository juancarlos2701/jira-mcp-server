"""General utility functions for interacting with the Jira API."""

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
) -> dict | list:
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


def get_projects() -> dict | list:
    """
    Get all projects from Jira.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    return jira_api_request(
        method="GET",
        endpoint="project",
    )


def get_priorities() -> dict | list:
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


def get_issue_statuses() -> dict | list:
    """
    Retrieve all issue statuses defined in the Jira instance.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    return jira_api_request(
        method="GET",
        endpoint="status",
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
