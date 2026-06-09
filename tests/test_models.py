import unittest
from models.project import Project
from models.task import Task
from models.user import User


class TestModels(unittest.TestCase):

    def test_user_creation_and_serialization(self):
        user = User(name="Test User", email="test@example.com")
        self.assertEqual(user.name, "Test User")
        self.assertEqual(user.email, "test@example.com")
        data = user.to_dict()
        restored = User.from_dict(data)
        self.assertEqual(restored.email, user.email)
        self.assertEqual(restored.id, user.id)

    def test_project_due_date_validation(self):
        project = Project(title="Build API", description="API project", due_date="2026-08-01", owner_id=1)
        self.assertEqual(project.due_date, "2026-08-01")
        with self.assertRaises(ValueError):
            Project(title="Bad Due", description="Invalid", due_date="08-01-2026", owner_id=1)

    def test_task_status_and_completion(self):
        task = Task(title="Write tests", project_id=1, status="pending")
        self.assertEqual(task.status, "pending")
        task.complete()
        self.assertEqual(task.status, "completed")
        with self.assertRaises(ValueError):
            task.status = "unknown"

if __name__ == "__main__":
    unittest.main()
