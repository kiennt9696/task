from abc import ABC, abstractmethod
from typing import List

from task.models import Task


class ITaskRepository(ABC):

    @abstractmethod
    def search_tasks(
        self, _from: int, size: int, filters: list, sort: list, counting: bool
    ) -> (List[Task], int):
        pass

    @abstractmethod
    def update_task(self, task_id: str, data: dict):
        pass

    @abstractmethod
    def create_task(self, task_info: dict) -> Task:
        pass

    @abstractmethod
    def get_employee_task_summary(
        self, _from: int, size: int, filters: list, sort: list
    ) -> List[dict]:
        pass
