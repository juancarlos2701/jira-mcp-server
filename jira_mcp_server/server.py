"""
Jira MCP Server module.

This module provides a FastMCP server for interacting with the Jira API.
"""
from dotenv import load_dotenv
from fastmcp import FastMCP

from tools import (
    get_projects,
    get_project_users,
    get_project_issues,
    get_project_issue_types,
    get_priorities,
    get_labels,
    get_issue_metadata,
    get_issue_fields,
    get_issue_statuses,
    create_issue,
    get_current_user,
)

load_dotenv()

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
        get_project_users,
        get_project_issues,
        get_project_issue_types,
        get_priorities,
        get_labels,
        get_issue_metadata,
        get_issue_fields,
        get_issue_statuses,
        create_issue,
        get_current_user,
    ],
)


if __name__ == "__main__":
    mcp.run()
