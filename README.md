# Jira MCP Server

This project provides a FastMCP server for interacting with the Jira API. It exposes a variety of tools for managing Jira projects, issues, and users.

## Available Tools

The server exposes the following tools:

### General Tools

*   `get_projects`: Retrieves all projects from Jira.
*   `get_priorities`: Returns the list of all usable issue priorities.
*   `get_labels`: Retrieves all labels available in Jira.
*   `get_issue_statuses`: Retrieves all issue statuses defined in the Jira instance.
*   `get_current_user`: Retrieves information about the currently authenticated Jira user.

### Project Tools

*   `get_project_users`: Get all users associated with a given Jira project.
*   `get_project_issues`: Get all issues for a given project from Jira.
*   `get_project_issue_types`: Retrieve all issue types available for a specific Jira project.

### Issue Tools

*   `get_issue_creation_metadata`: Retrieve issue creation metadata for a specific project and issue type.
*   `create_issue`: Create a new Jira issue.
*   `get_issue`: Get details for a specific issue.
*   `change_issue_title`: Change the summary/title of a Jira issue.
*   `change_issue_description`: Change the description of a Jira issue.
*   `change_issue_reporter`: Change the reporter of a Jira issue.
*   `change_issue_priority`: Change the priority of a Jira issue.
*   `change_issue_environment`: Change the environment field of a Jira issue.
*   `add_issue_labels`: Add one or more labels to a Jira issue.
*   `change_issue_labels`: Replace all labels of a Jira issue with a new set of labels.
*   `remove_issue_labels`: Remove one or more labels from a Jira issue.
*   `update_issue_duedate`: Update the due date of a Jira issue.
*   `get_issue_link_types`: Returns the list of all available issue link types
*   `link_issues`: Link two issues together.
*   `delete_issues_link`: Delete a link between two issues.
*   `delete_issue`: Delete a Jira issue.
*   `assign_issue`: Assign a Jira issue to a user.
*   `comment_issue`: Add a comment to a Jira issue.

## Docker

This project includes a `Dockerfile` to build and run the MCP server in a container.

### Dockerfile Explained

The `Dockerfile` is structured in multiple stages to optimize the build process and create a small, efficient final image.

1.  **Base Image**: It starts with `ghcr.io/astral-sh/uv:python3.13-alpine`, a lightweight Python image that comes with `uv` pre-installed.
2.  **Install Dependencies**: It then copies the `uv.lock` and `pyproject.toml` files and installs the dependencies using `uv sync`. This leverages Docker's layer caching, so dependencies are only re-installed when these files change.
3.  **Copy Source Code**: The rest of the application source code is then copied into the image.
4.  **Install Project**: The project itself is installed.
5.  **Set `PATH`**: The `PATH` environment variable is updated to include the virtual environment's `bin` directory, so the `fastmcp` executable can be run directly.
6.  **Entrypoint**: The `ENTRYPOINT` is set to run the MCP server using `fastmcp run jira_mcp_server/server.py`.

### Building the Docker Image

To build the Docker image, run the following command from the root of the project:

```bash
docker build -t jira-mcp-server .
```

### Running the Docker Container

To run the Docker container, you will need to provide the necessary environment variables. You can do this by creating a `.env` file in the root of the project with the following content:

```
JIRA_BASE_URL=https://your-jira-instance.atlassian.net/rest/api/3/
JIRA_USER=your-jira-username
JIRA_API_KEY=your-jira-api-key
REQUESTS_TIMEOUT=30

# Logging configuration
# LOG_LEVEL can be DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO
# LOG_FILE is the name of the log file. If provided, logs will be written to /app/logs/<LOG_FILE> inside the container.
# If not provided, logs will be sent to stderr.
# LOG_FILE=jira_mcp_server.log
```

Then, you can run the mcp-server using the default `stdio` transport with the following command:

```bash
docker run --rm -i --env-file path/to/.env jira-mcp-server
```

To enable file logging and persist logs outside the container, you need to:
1.  Uncomment and set `LOG_FILE` in your `.env` file (e.g., `LOG_FILE=jira_mcp_server.log`).
2.  Mount a local volume to the `/app/logs` directory inside the container.

For example, to store logs in a local folder named `my_local_logs_folder`:

```bash
docker run --rm -i --env-file path/to/.env -v my_local_logs_folder:/app/logs jira-mcp-server
```
