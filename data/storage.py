from __future__ import annotations
import json
from pathlib import Path
from typing import Any

from models.project import Project
from models.task import Task
from models.user import User


class Storage:
    """Handles JSON persistence for users, projects, and tasks."""

    def __init__(self, data_path: Path | str = None) -> None:
        """Initialize storage and load persisted data from the configured file."""
        self.base_path = Path(data_path) if data_path is not None else Path(__file__).resolve().parent
        if self.base_path.is_dir() or self.base_path.suffix.lower() != ".json":
            self.file_path = self.base_path / "data.json"
        else:
            self.file_path = self.base_path
        self.users: list[User] = []
        self.projects: list[Project] = []
        self.tasks: list[Task] = []
        self.load()

    def load(self) -> None:
        """Load persisted JSON data from disk, handling missing or malformed files gracefully."""
        if not self.file_path.exists():
            self._initialize_empty_file()
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except (json.JSONDecodeError, OSError):
            self._initialize_empty_file()
            return

        self.users = [User.from_dict(item) for item in payload.get("users", [])]
        self.projects = [Project.from_dict(item) for item in payload.get("projects", [])]
        self.tasks = [Task.from_dict(item) for item in payload.get("tasks", [])]

    def save(self) -> None:
        """Persist the current object collections to the JSON file."""
        content = {
            "users": [user.to_dict() for user in self.users],
            "projects": [project.to_dict() for project in self.projects],
            "tasks": [task.to_dict() for task in self.tasks],
        }
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as handle:
            json.dump(content, handle, indent=2)

    def _initialize_empty_file(self) -> None:
        """Create a fresh JSON store when data is missing or corrupted."""
        self.users = []
        self.projects = []
        self.tasks = []
        self.save()

    def add_user(self, user: User) -> User:
        """Add a user to storage and persist the change."""
        self.users.append(user)
        self.save()
        return user

    def add_project(self, project: Project) -> Project:
        """Add a project and persist the change."""
        self.projects.append(project)
        owner = self.get_user_by_id(project.owner_id)
        if owner:
            owner.project_ids.append(project.id)
        self.save()
        return project

    def add_task(self, task: Task) -> Task:
        """Add a task, associate it with its project, and persist."""
        self.tasks.append(task)
        project = self.get_project_by_id(task.project_id)
        if project:
            project.add_task(task.id)
        self.save()
        return task

    def get_user_by_id(self, user_id: int) -> User | None:
        """Retrieve a user by ID."""
        return next((user for user in self.users if user.id == user_id), None)

    def get_project_by_id(self, project_id: int) -> Project | None:
        """Retrieve a project by ID."""
        return next((project for project in self.projects if project.id == project_id), None)

    def get_task_by_id(self, task_id: int) -> Task | None:
        """Retrieve a task by ID."""
        return next((task for task in self.tasks if task.id == task_id), None)

    def find_user_by_email(self, email: str) -> User | None:
        """Find a user by their email address."""
        normalized = email.strip().lower()
        return next((user for user in self.users if user.email == normalized), None)

    def list_projects_for_user(self, user_id: int) -> list[Project]:
        """Return projects owned by the specified user."""
        return [project for project in self.projects if project.owner_id == user_id]

    def list_tasks_for_project(self, project_id: int) -> list[Task]:
        """Return tasks associated with the specified project."""
        return [task for task in self.tasks if task.project_id == project_id]

    def list_tasks_for_user(self, user_id: int) -> list[Task]:
        """Return tasks assigned to the specified user."""
        return [task for task in self.tasks if user_id in task.assigned_to]
