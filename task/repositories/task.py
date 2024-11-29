from uuid import uuid4

from sqlalchemy import and_, func, case
from typing import List

from sqlalchemy.orm import Session

from task.infras.db.connection import DBConnectionHandler
from task.interfaces.repositories.task import ITaskRepository
from task.models import Task, User

COMPLETED = 4
EMPLOYEE_ROLE = "Employee"


class TaskRepository(ITaskRepository):
    def __init__(self, db: DBConnectionHandler):
        self.session: Session = db.session

    def search_tasks(
        self, _from: int, size: int, filters: list, sort: list, counting=False
    ) -> (List[Task], int):

        task_query = self.session.query(Task).filter(and_(*filters))
        total = 0
        if counting:
            total = task_query.count()
        if sort:
            task_query = task_query.order_by(*sort)
        return task_query.offset(_from).limit(size).all(), total

    def update_task(self, task_id: str, data: dict):
        task = self.session.query(Task).filter_by(id=task_id).first()
        for key, val in data.items():
            if hasattr(task, key):
                setattr(task, key, val)
        self.session.commit()

    def create_task(self, task_info: dict) -> Task:
        task = Task(**task_info)
        task.id = str(uuid4())
        self.session.add(task)
        self.session.commit()
        return task

    def get_employee_task_summary(
        self, _from: int, size: int, filters: list, sort: list
    ) -> List[dict]:
        result = (
            self.session.query(
                User.username,
                func.count(Task.id).label("total_tasks"),
                func.count(case((Task.status_id == COMPLETED, 1))).label(
                    "completed_tasks"
                ),
            )
            .outerjoin(Task, User.username == Task.assignee)
            .filter(User.role == EMPLOYEE_ROLE)
            .group_by(User.username)
            .order_by(*sort)
            .offset(_from)
            .limit(size)
        )
        return result.all()
