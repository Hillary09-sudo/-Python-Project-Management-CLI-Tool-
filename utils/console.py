from __future__ import annotations
from rich.console import Console
from rich.table import Table

console = Console()


def display_users(users: list) -> None:
    """Render a table of users to the console."""
    table = Table(title="Users")
    table.add_column("ID", justify="right")
    table.add_column("Name")
    table.add_column("Email")
    for user in users:
        table.add_row(str(user.id), user.name, user.email)
    console.print(table)


def display_projects(projects: list, users: dict[int, str]) -> None:
    """Render a table of projects with owner name information."""
    table = Table(title="Projects")
    table.add_column("ID", justify="right")
    table.add_column("Title")
    table.add_column("Owner")
    table.add_column("Due Date")
    table.add_column("Status")
    for project in projects:
        owner_name = users.get(project.owner_id, "Unknown")
        status = "Overdue" if project.is_overdue() else "Open"
        table.add_row(str(project.id), project.title, owner_name, project.due_date, status)
    console.print(table)


def display_tasks(tasks: list, users: dict[int, str]) -> None:
    """Render a table of tasks with assigned user details."""
    table = Table(title="Tasks")
    table.add_column("ID", justify="right")
    table.add_column("Title")
    table.add_column("Project ID", justify="right")
    table.add_column("Status")
    table.add_column("Assigned To")
    for task in tasks:
        contributors = ", ".join(users.get(uid, "Unknown") for uid in task.assigned_to) or "Unassigned"
        table.add_row(str(task.id), task.title, str(task.project_id), task.status.title(), contributors)
    console.print(table)
