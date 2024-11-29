from task.interfaces.repositories.workflow import IWorkflowRepository
from task.models import Transition


class WorkflowService:
    def __init__(self, workflow_repo: IWorkflowRepository):
        self.workflow_repo = workflow_repo

    def is_valid_transition(
        self, workflow_id, from_status_id, to_status_id, current_user
    ):
        conditions = [
            Transition.workflow_id == workflow_id,
            Transition.from_status_id == from_status_id,
            Transition.to_status_id == to_status_id,
        ]
        transition, _ = self.workflow_repo.search_transition(conditions, False)
        if not transition:
            return False
        if not transition[0].approver:
            return True
        return transition[0].approver == current_user.get("username")
