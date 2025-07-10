"""
Jira MCP Server module.

This module provides a FastMCP server for interacting with the Jira API.
"""

from dotenv import load_dotenv
from fastmcp import FastMCP

from config.logging import setup_logging

from jira_api_tools.general import (
    get_projects,
    get_priorities,
    get_labels,
    get_issue_statuses,
    get_current_user,
)
from jira_api_tools.project import (
    get_project_users,
    get_project_issues,
    get_project_issue_types,
)
from jira_api_tools.issue import (
    get_issue_creation_metadata,
    create_issue,
    get_issue,
    change_issue_title,
    change_issue_description,
    change_issue_reporter,
    change_issue_priority,
    change_issue_environment,
    add_issue_labels,
    change_issue_labels,
    remove_issue_labels,
    update_issue_duedate,
    get_issue_link_types,
    link_issues,
    delete_issues_link,
    delete_issue,
    assign_issue,
    comment_issue,
)

load_dotenv()
setup_logging()

mcp = FastMCP(
    name="Jira API - MCP Server",
    instructions="""
        This server provides tools to interact with the Jira API.
        You can use the tools to get information about Jira projects, issues, and more.
        You can also use the tools to create and update issues.
        You can also use the tools to search for issues.
        You can also use the tools to get information about Jira users.
        You can also use the tools to get information about Jira groups.
    """,
    tools=[
        get_projects,
        get_priorities,
        get_labels,
        get_issue_statuses,
        get_current_user,
        get_project_users,
        get_project_issues,
        get_project_issue_types,
        get_issue_creation_metadata,
        create_issue,
        get_issue,
        change_issue_title,
        change_issue_description,
        change_issue_reporter,
        change_issue_priority,
        change_issue_environment,
        add_issue_labels,
        change_issue_labels,
        remove_issue_labels,
        update_issue_duedate,
        get_issue_link_types,
        link_issues,
        delete_issues_link,
        delete_issue,
        assign_issue,
        comment_issue,
    ],
)


if __name__ == "__main__":
    mcp.run()
