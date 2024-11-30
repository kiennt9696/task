import unittest
from unittest.mock import MagicMock
from task.services import WorkflowService


class TestWorkflowService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = WorkflowService(workflow_repo=self.mock_repo)

    def test_is_valid_transition_no_transition(self):
        # Mock search_transition to return no results
        self.mock_repo.search_transition.return_value = ([], None)

        result = self.service.is_valid_transition(1, 2, 3, {"username": "test_user"})

        self.assertFalse(result)

    def test_is_valid_transition_no_approver(self):
        # Mock search_transition to return a transition with no approver
        mock_transition = MagicMock()
        mock_transition.approver = None
        self.mock_repo.search_transition.return_value = ([mock_transition], None)

        result = self.service.is_valid_transition(1, 2, 3, {"username": "test_user"})

        self.assertTrue(result)

    def test_is_valid_transition_with_approver_valid_user(self):
        # Mock search_transition to return a transition with an approver
        mock_transition = MagicMock()
        mock_transition.approver = "test_user"
        self.mock_repo.search_transition.return_value = ([mock_transition], None)

        result = self.service.is_valid_transition(1, 2, 3, {"username": "test_user"})

        self.assertTrue(result)

    def test_is_valid_transition_with_approver_invalid_user(self):
        # Mock search_transition to return a transition with an approver
        mock_transition = MagicMock()
        mock_transition.approver = "another_user"
        self.mock_repo.search_transition.return_value = ([mock_transition], None)

        result = self.service.is_valid_transition(1, 2, 3, {"username": "test_user"})

        self.assertFalse(result)

