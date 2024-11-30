import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from task.models import Transition
from task.infras.db.connection import DBConnectionHandler
from task.repositories import WorkflowRepository


class TestWorkflowRepository(unittest.TestCase):

    def setUp(self):
        self.mock_db = MagicMock(DBConnectionHandler)
        self.mock_session = MagicMock(Session)
        self.mock_db.session = self.mock_session
        self.repo = WorkflowRepository(self.mock_db)

    def test_is_valid_transition(self):
        """
        Mock order: query -> filter -> (count) -> (order) -> offset -> limit -> all
        :return:
        """

        mock_transition = MagicMock(Transition)
        self.mock_session.query.return_value.filter.return_value.all.return_value = [mock_transition]

        filters = []
        transitions, _ = self.repo.search_transition(filters, False)

        # Assertions
        self.assertEqual(transitions, [mock_transition])

    def test_is_valid_transition_with_counting(self):
        """
        Mock order: query -> filter -> (count) -> (order) -> offset -> limit -> all
        :return:
        """

        mock_transition = MagicMock(Transition)
        self.mock_session.query.return_value.filter.return_value.count.return_value = 10

        filters = []
        _, count = self.repo.search_transition(filters, True)

        # Assertions
        self.assertEqual(count, 10)


