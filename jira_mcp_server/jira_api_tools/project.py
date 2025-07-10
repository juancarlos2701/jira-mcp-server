"""Functions for interacting with Jira projects via the API."""

import logging
from http import HTTPMethod
from .general import jira_api_request

logger = logging.getLogger(__name__)


def get_project_users(project_keys: str) -> dict | list:
    """
    Get all users associated with a given Jira project.
    :API Docs: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-user-search/#api-rest-api-3-user-assignable-multiprojectsearch-get

    :param project_key: Key of the Jira project.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    logger.info("Getting users for project %s", project_keys)
    query_params = {"projectKeys": project_keys}

    return jira_api_request(
        method=HTTPMethod.GET,
        endpoint="user/assignable/multiProjectSearch",
        params=query_params,
    )


def get_project_issues(project_key: str) -> dict:
    """
    Get all issues for a given project from Jira.
    :API Docs: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-issue-picker-get

    :param project_key: Key of the Jira project

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    logger.info("Getting issues for project %s", project_key)
    query_params = {"currentProjectId": project_key}

    return jira_api_request(
        method=HTTPMethod.GET,
        endpoint="issue/picker",
        params=query_params,
    )


def get_project_issue_types(project_key: str, max_results: int = 50) -> dict:
    """
    Retrieve all issue types available for a specific Jira project.
    :API Docs: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-createmeta-projectidorkey-issuetypes-get

    :param project_key: Key of the Jira project.
    :param max_results: Maximum number of issue types to return.

    :return: The JSON-decoded response from the Jira API if the request is successful,
             otherwise a dictionary containing the status code, response text, and reason.
    """
    logger.info("Getting issue types for project %s", project_key)
    logger.debug("max_results: %s", max_results)
    query_params = {"maxResults": max_results}

    return jira_api_request(
        method=HTTPMethod.GET,
        endpoint=f"issue/createmeta/{project_key}/issuetypes",
        params=query_params,
    )
