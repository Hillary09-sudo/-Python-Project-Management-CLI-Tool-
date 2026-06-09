import argparse
import unittest

from main import build_parser


class TestCLI(unittest.TestCase):

    def test_parser_add_user(self):
        parser = build_parser()
        args = parser.parse_args(["add-user", "--name", "Sam", "--email", "sam@example.com"])
        self.assertEqual(args.command, "add-user")
        self.assertEqual(args.name, "Sam")
        self.assertEqual(args.email, "sam@example.com")

    def test_parser_add_project(self):
        parser = build_parser()
        args = parser.parse_args([
            "add-project",
            "--email",
            "sam@example.com",
            "--title",
            "New Project",
            "--description",
            "Details",
            "--due-date",
            "2026-09-15",
        ])
        self.assertEqual(args.command, "add-project")
        self.assertEqual(args.title, "New Project")
        self.assertEqual(args.due_date, "2026-09-15")

    def test_parser_complete_task(self):
        parser = build_parser()
        args = parser.parse_args(["complete-task", "--task-id", "2"])
        self.assertEqual(args.command, "complete-task")
        self.assertEqual(args.task_id, 2)
