import unittest
from unittest.mock import MagicMock, patch
from uuid import uuid4
from sqlalchemy.orm import Session
from task.models import Task, User
from task.infras.db.connection import DBConnectionHandler
from task.repositories.task import TaskRepository


class MockQuery:
    def __init__(self, return_value):
        self.data = return_value

    def all(self):
        return self.data


class TestTaskRepository(unittest.TestCase):

    def setUp(self):
        self.mock_db = MagicMock(DBConnectionHandler)
        self.mock_session = MagicMock(Session)
        self.mock_db.session = self.mock_session
        self.repo = TaskRepository(self.mock_db)

    def test_search_tasks(self):
        """
        Mock order: query -> filter -> (count) -> (order) -> offset -> limit -> all
        :return:
        """

        mock_task = MagicMock(Task)
        self.mock_session.query.return_value.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = [
            mock_task
        ]

        filters = []
        sort = [MagicMock()]
        tasks, total = self.repo.search_tasks(0, 10, filters, sort)

        # Assertions
        self.assertEqual(tasks, [mock_task])

    def test_update_task(self):
        mock_task = MagicMock(Task)
        self.mock_session.query.return_value.filter_by.return_value.first.return_value = (
            mock_task
        )

        task_id = str(uuid4())
        data = {"name": "Updated Task"}
        self.repo.update_task(task_id, data)

        for key, value in data.items():
            setattr(mock_task, key, value)

        self.mock_session.commit.assert_called()

    def test_create_task(self):
        mock_task_info = {"title": "New Task", "assignee": "test_user"}

        with patch("task.repositories.task.uuid4", return_value=uuid4()):
            task = self.repo.create_task(mock_task_info)

        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, mock_task_info["title"])
        self.mock_session.add.assert_called_with(task)
        self.mock_session.commit.assert_called()

    def test_get_employee_task_summary(self):
        mock_result = MockQuery(("test_user", 5, 3))
        self.mock_session.query.return_value.outerjoin.return_value.filter.return_value.group_by.return_value.order_by.return_value.offset.return_value.limit.return_value = (
            mock_result
        )

        filters = [MagicMock()]
        sort = [MagicMock()]
        result = self.repo.get_employee_task_summary(0, 10, filters, sort)

        self.assertEqual(result, mock_result.data)
