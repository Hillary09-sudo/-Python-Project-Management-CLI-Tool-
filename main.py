from __future__ import annotations
import argparse
from pathlib import Path
from typing import Iterable

from data.storage import Storage
from models.project import Project
from models.task import Task
from models.user import User
from utils.console import console, display_projects, display_tasks, display_users
from utils.validation import parse_date, validate_email


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        description="Project Management CLI Tool for managing users, projects, and tasks."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    user_parser = subparsers.add_parser("add-user", help="Create a new user.")
    user_parser.add_argument("--name", required=True, help="Full name of the user.")
    user_parser.add_argument("--email", required=True, help="Email address of the user.")

    subparsers.add_parser("list-users", help="Display all users.")

    project_parser = subparsers.add_parser("add-project", help="Add a project for a user.")
    project_parser.add_argument("--email", required=True, help="Owner user email.")
    project_parser.add_argument("--title", required=True, help="Project title.")
    project_parser.add_argument("--description", required=True, help="Project description.")
    project_parser.add_argument("--due-date", required=True, help="Due date in YYYY-MM-DD format.")

    list_projects = subparsers.add_parser("list-projects", help="List all projects or by user email.")
    list_projects.add_argument("--email", help="Filter projects by owner email.")

    show_projects = subparsers.add_parser("show-user-projects", help="Show projects for a specific user.")
    show_projects.add_argument("--email", required=True, help="Owner user email.")

    task_parser = subparsers.add_parser("add-task", help="Add a task to a project.")
    task_parser.add_argument("--project-id", type=int, required=True, help="Project ID to attach the task.")
    task_parser.add_argument("--title", required=True, help="Task title.")
    task_parser.add_argument("--status", default="pending", help="Task status: pending, in progress, or completed.")
    task_parser.add_argument("--assigned-to", help="Comma-separated emails of users assigned to the task.")

    subparsers.add_parser("list-tasks", help="List all tasks.")

    complete_parser = subparsers.add_parser("complete-task", help="Mark a task as completed.")
    complete_parser.add_argument("--task-id", type=int, required=True, help="Task ID to complete.")

    return parser


def parse_assigned_users(storage: Storage, assigned_to: str | None) -> list[int]:
    """Convert a comma-separated list of emails into validated user IDs."""
    if not assigned_to:
        return []
    user_ids: list[int] = []
    for email in assigned_to.split(","):
        normalized = email.strip().lower()
        if not validate_email(normalized):
            raise ValueError(f"Invalid email address: {email}")
        user = storage.find_user_by_email(normalized)
        if not user:
            raise ValueError(f"No user found with email: {email}")
        if user.id not in user_ids:
            user_ids.append(user.id)
    return user_ids


def run_command(args: argparse.Namespace, storage: Storage) -> None:
    """Execute the selected CLI command against the storage backend."""
    if args.command == "add-user":
        if not validate_email(args.email):
            raise ValueError("Please provide a valid email address.")
        user = User(name=args.name, email=args.email)
        storage.add_user(user)
        console.print(f"[green]Created user:[/] {user}")

    elif args.command == "list-users":
        display_users(storage.users)

    elif args.command == "add-project":
        if not validate_email(args.email):
            raise ValueError("Please provide a valid email address for the project owner.")
        owner = storage.find_user_by_email(args.email)
        if not owner:
            raise ValueError(f"No user found with email: {args.email}")
        due_date = parse_date(args.due_date)
        project = Project(
            title=args.title,
            description=args.description,
            due_date=due_date,
            owner_id=owner.id,
        )
        storage.add_project(project)
        console.print(f"[green]Created project:[/] {project.title} (ID {project.id})")

    elif args.command == "list-projects":
        projects = storage.projects
        if args.email:
            owner = storage.find_user_by_email(args.email)
            if not owner:
                raise ValueError(f"No user found with email: {args.email}")
            projects = storage.list_projects_for_user(owner.id)
        user_map = {user.id: user.name for user in storage.users}
        display_projects(projects, user_map)

    elif args.command == "show-user-projects":
        owner = storage.find_user_by_email(args.email)
        if not owner:
            raise ValueError(f"No user found with email: {args.email}")
        projects = storage.list_projects_for_user(owner.id)
        display_projects(projects, {owner.id: owner.name})

    elif args.command == "add-task":
        project = storage.get_project_by_id(args.project_id)
        if not project:
            raise ValueError(f"Project with ID {args.project_id} does not exist.")
        assigned_ids = parse_assigned_users(storage, args.assigned_to)
        task = Task(
            title=args.title,
            project_id=project.id,
            assigned_to=assigned_ids,
            status=args.status,
        )
        storage.add_task(task)
        console.print(f"[green]Created task:[/] {task.title} (ID {task.id})")

    elif args.command == "list-tasks":
        user_map = {user.id: user.name for user in storage.users}
        display_tasks(storage.tasks, user_map)

    elif args.command == "complete-task":
        task = storage.get_task_by_id(args.task_id)
        if not task:
            raise ValueError(f"Task with ID {args.task_id} does not exist.")
        task.complete()
        storage.save()
        console.print(f"[green]Task completed:[/] {task.title} (ID {task.id})")

    else:
        raise ValueError(f"Unknown command: {args.command}")


def main(argv: list[str] | None = None) -> None:
    """Entry point for invoking the CLI from the command line."""
    parser = build_parser()
    args = parser.parse_args(argv)
    storage_dir = Path(__file__).resolve().parent / "data"
    storage = Storage(data_path=storage_dir)
    try:
        run_command(args, storage)
    except ValueError as exc:
        console.print(f"[red]Error:[/] {exc}")


if __name__ == "__main__":
    main()
