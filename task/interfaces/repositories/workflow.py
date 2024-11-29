from abc import ABC, abstractmethod

from task.models import Transition


class IWorkflowRepository(ABC):

    @abstractmethod
    def search_transition(
        self, conditions: list, counting: bool
    ) -> (list[Transition], int):
        pass
