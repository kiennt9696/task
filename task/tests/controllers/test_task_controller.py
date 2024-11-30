from unittest.mock import patch, MagicMock
from task.tests import BaseTestCase


class TestTaskController(BaseTestCase):

    @patch("task.controllers.task.get_current_user")
    @patch("task.controllers.task.task_service.get_personal_tasks")
    def test_get_personal_tasks(self, mock_get_personal_tasks, mock_get_current_user):
        mock_get_current_user.return_value = {"username": "test_user"}
        mock_get_personal_tasks.return_value = ([], 0)
        with self.app.test_client() as client:
            response = client.post(
                "/tasks/personal",
                json={
                    "_from": 0,
                    "size": 10,
                    "start_date": "2023-01-01",
                    "end_date": "2023-12-31",
                    "counting": True,
                },
                headers={"Authorization": "Bearer mocked_token"}
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"tasks": [], "count": 0})

    @patch("task.controllers.task.task_service.get_all_tasks")
    def test_get_all_tasks(self, mock_get_all_tasks):
        mock_get_all_tasks.return_value = ([], 0)

        response = self.client.post(
            "/tasks/all",
            json={
                "_from": 0,
                "size": 10,
                "start_date": "2023-01-01",
                "end_date": "2023-12-31",
                "counting": True,
                "query": {},
                "sort": "-created_at",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"tasks": [], "count": 0})

    @patch("task.controllers.task.get_current_user")
    @patch("task.controllers.task.task_service.update_assigned_task_only")
    def test_update_assigned_task_only(self, mock_update_task, mock_get_current_user):
        mock_get_current_user.return_value = {"username": "test_user"}
        mock_update_task.return_value = None

        response = self.client.post(
            "/tasks/task123/update", json={"status_id": 4}, headers={"Authorization": "Bearer mocked_token"}
        )
        self.assertEqual(response.status_code, 204)

    @patch("task.controllers.task.task_service.update_task_by_manager")
    def test_assign_task_by_manager(self, mock_update_task):
        mock_update_task.return_value = None

        response = self.client.post(
            "/tasks/assign",
            json={"task_id": "task123", "assignee": "test_user", "due_date": "2023-12-31"},
        )
        self.assertEqual(response.status_code, 204)

    @patch("task.controllers.task.task_service.create_task")
    def test_create_task(self, mock_create_task):
        mock_task = MagicMock()
        mock_task.id = "task123"
        mock_create_task.return_value = mock_task

        response = self.client.post(
            "/tasks/create",
            json={"name": "Test Task", "assignee": "test_user", "due_date": "2023-12-31"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"task_id": "task123"})

    @patch("task.controllers.task.task_service.view_employee_task_report")
    def test_get_employee_task_summary(self, mock_employee_summary):
        mock_employee_summary.return_value = [["test_user", 10, 5]]

        response = self.client.post(
            "/tasks/employee-summary",
            json={
                "_from": 0,
                "size": 10,
                "start_date": "2023-01-01",
                "end_date": "2023-12-31",
                "query": {},
                "sort": "-created_at",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"report": [["test_user", 10, 5]]})

