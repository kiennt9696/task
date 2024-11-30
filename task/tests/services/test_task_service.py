import unittest
from unittest.mock import MagicMock, patch
from task.models import Task
from common_utils.exception import Forbidden, InvalidParameter

from task.services import TaskService


class TestTaskService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.mock_workflow_service = MagicMock()
        self.service = TaskService(task_repo=self.mock_repo, workflow_service=self.mock_workflow_service)

    @patch("helpers.util.convert_str2time")
    @patch("helpers.util.parse_sort_query")
    def test_get_personal_tasks(self, mock_parse_sort_query, mock_convert_str2time):
        # Mock helper functions
        mock_convert_str2time.side_effect = lambda x: x
        mock_parse_sort_query.return_value = []

        # Mock repository response
        mock_tasks = [MagicMock(Task)]
        self.mock_repo.search_tasks.return_value = (mock_tasks, 1)

        current_user = {"username": "test_user"}
        tasks, count = self.service.get_personal_tasks(
            current_user, 0, 10, "2023-01-01 00:00:00", "2023-12-31 00:00:00", True
        )

        self.assertEqual(len(tasks), 1)
        self.assertEqual(count, 1)
        self.mock_repo.search_tasks.assert_called_once()

    @patch("helpers.util.convert_str2time")
    @patch("helpers.util.parse_sort_query")
    def test_get_all_tasks(self, mock_parse_sort_query, mock_convert_str2time):
        # Mock helper functions
        mock_convert_str2time.side_effect = lambda x: x
        mock_parse_sort_query.return_value = []

        # Mock repository response
        mock_tasks = [MagicMock(Task)]
        self.mock_repo.search_tasks.return_value = (mock_tasks, 1)

        query = {"assignee": "test_assignee"}
        sorts = "-created_at"
        tasks, count = self.service.get_all_tasks(
            0, 10, "2023-01-01 00:00:00", "2023-12-31 00:00:00", query, sorts, True
        )

        self.assertEqual(len(tasks), 1)
        self.assertEqual(count, 1)
        self.mock_repo.search_tasks.assert_called_once()

    def test_update_assigned_task_only_task_not_found(self):
        self.mock_repo.search_tasks.return_value = ([], 0)

        with self.assertRaises(Forbidden):
            self.service.update_assigned_task_only({"username": "test_user"}, "task_id", 2)

    def test_update_assigned_task_only_invalid_transition(self):
        mock_task = MagicMock(Task)
        mock_task.status_id = 1
        mock_task.task_type.workflow_id = 10
        self.mock_repo.search_tasks.return_value = ([mock_task], 0)

        self.mock_workflow_service.is_valid_transition.return_value = False

        with self.assertRaises(InvalidParameter):
            self.service.update_assigned_task_only({"username": "test_user"}, "task_id", 2)

    def test_update_assigned_task_only_success(self):
        mock_task = MagicMock(Task)
        mock_task.status_id = 1
        mock_task.task_type.workflow_id = 10
        self.mock_repo.search_tasks.return_value = ([mock_task], 0)

        self.mock_workflow_service.is_valid_transition.return_value = True

        result = self.service.update_assigned_task_only({"username": "test_user"}, "task_id", 2)

        self.assertIsNotNone(result)
        self.mock_repo.update_task.assert_called_with("task_id", {"status_id": 2})

    def test_create_task(self):
        task_info = {"title": "Test Task", "unknown_field": "value"}
        self.mock_repo.create_task.return_value = MagicMock(Task)

        result = self.service.create_task(task_info)

        self.assertIsNotNone(result)
        self.assertNotIn("unknown_field", task_info)
        self.mock_repo.create_task.assert_called_once()

    @patch("helpers.util.convert_str2time")
    @patch("helpers.util.parse_sort_query")
    def test_view_employee_task_report(self, mock_parse_sort_query, mock_convert_str2time):
        mock_convert_str2time.side_effect = lambda x: x
        mock_parse_sort_query.return_value = []

        mock_summary = [("employee1", 10, 5)]
        self.mock_repo.get_employee_task_summary.return_value = mock_summary

        result = self.service.view_employee_task_report(0, 10, {}, "2023-01-01 00:00:00", "2023-12-31 00:00:00", "-created_at")

        self.assertEqual(result, [["employee1", 10, 5]])
        self.mock_repo.get_employee_task_summary.assert_called_once()


