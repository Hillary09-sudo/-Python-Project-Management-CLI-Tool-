import tempfile
import unittest
from pathlib import Path

from data.storage import Storage
from models.project import Project
from models.task import Task
from models.user import User


class TestStorage(unittest.TestCase):

    def test_add_and_retrieve_entities(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = Storage(data_path=Path(temp_dir))
            user = store.add_user(User(name="Test", email="test@example.com"))
            project = store.add_project(Project(title="Demo", description="Demo project", due_date="2026-09-01", owner_id=user.id))
            task = store.add_task(Task(title="Task 1", project_id=project.id, assigned_to=[user.id]))

            reloaded = Storage(data_path=Path(temp_dir))
            self.assertEqual(len(reloaded.users), 1)
            self.assertEqual(reloaded.users[0].email, "test@example.com")
            self.assertEqual(reloaded.projects[0].title, "Demo")
            self.assertEqual(reloaded.tasks[0].title, "Task 1")

    def test_list_functions(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = Storage(data_path=Path(temp_dir))
            user = store.add_user(User(name="Alpha", email="alpha@example.com"))
            project = store.add_project(Project(title="Alpha Project", description="Desc", due_date="2026-11-01", owner_id=user.id))
            task = store.add_task(Task(title="Alpha Task", project_id=project.id, assigned_to=[user.id]))

            self.assertEqual(store.list_projects_for_user(user.id), [project])
            self.assertEqual(store.list_tasks_for_project(project.id), [task])
            self.assertEqual(store.list_tasks_for_user(user.id), [task])
