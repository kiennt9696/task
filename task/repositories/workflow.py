from sqlalchemy.orm import Session

from task.infras.db.connection import DBConnectionHandler
from task.interfaces.repositories.workflow import IWorkflowRepository
from task.models import Transition


class WorkflowRepository(IWorkflowRepository):
    def __init__(self, db: DBConnectionHandler):
        self.session: Session = db.session

    def search_transition(
        self, conditions: list, counting: bool
    ) -> (list[Transition], int):
        query = self.session.query(Transition).filter(*conditions)
        if counting:
            return [], query.count()
        return query.all(), 0
