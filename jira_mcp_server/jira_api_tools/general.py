"""General utility functions for interacting with the Jira API."""

import logging
import os
from http import HTTPMethod
from urllib.parse import urljoin
from typing import Optional
import requests
from requests.auth import HTTPBasicAuth

JIRA_AUTH = HTTPBasicAuth(str(os.getenv("JIRA_USER")), str(os.getenv("JIRA_API_KEY")))
logger = logging.getLogger(__name__)


def jira_api_request(
    method: HTTPMethod,
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
    logger.info("Requesting %s on %s", method, endpoint)
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
        logger.info("Request successful with status code %s", response.status_code)
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            logger.warning("Failed to decode JSON from response")
            return {
                "successful": response.ok,
                "status_code": response.status_code,
                "text": response.text,
                "reason": response.reason,
            }
    else:
        logger.error("Request failed with status code %s: %s", response.status_code, response.text)
        return {
            "successful": response.ok,
            "status_code": response.status_code,
            "text": response.text,
            "reason": response.reason,
        }


def get_projects() -> dict | list:
    """
    Get all projects from Jira.
    :API Docs: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-projects/#api-rest-api-3-project-get

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    logger.info("Getting all projects")
    return jira_api_request(
        method=HTTPMethod.GET,
        endpoint="project",
    )


def get_priorities() -> dict | list:
    """
    Returns the list of all usable issue priorities.
    :API Docs: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-priorities/#api-rest-api-3-priority-get

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    logger.info("Getting all priorities")
    return jira_api_request(
        method=HTTPMethod.GET,
        endpoint="priority",
    )


def get_labels(max_results: int = 50) -> dict:
    """
    Retrieve all labels available in Jira.
    :API Docs: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-labels/#api-rest-api-3-label-get

    :param max_results: Maximum number of labels to return.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    logger.info("Getting labels with max_results=%s", max_results)
    query_params = {"maxResults": max_results}

    return jira_api_request(
        method=HTTPMethod.GET,
        endpoint="label",
        params=query_params,
    )


def get_issue_statuses() -> dict | list:
    """
    Retrieve all issue statuses defined in the Jira instance.
    :API Docs: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-workflow-statuses/#api-rest-api-3-status-get

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    logger.info("Getting all issue statuses")
    return jira_api_request(
        method=HTTPMethod.GET,
        endpoint="status",
    )


def get_current_user() -> dict:
    """
    Retrieve information about the currently authenticated Jira user.
    :API Docs: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-myself/#api-rest-api-3-myself-get

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    logger.info("Getting current user")
    return jira_api_request(
        method=HTTPMethod.GET,
        endpoint="myself",
    )
