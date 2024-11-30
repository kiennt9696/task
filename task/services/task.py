from common_utils.exception import Forbidden, InvalidParameter

from helpers.util import convert_str2time, parse_sort_query
from task.interfaces.repositories.task import ITaskRepository
from task.models import Task
from task.schemas.schema import TaskSchema


class TaskService:
    def __init__(self, task_repo: ITaskRepository, workflow_service):
        self.task_repo = task_repo
        self.workflow_service = workflow_service

    def __dump_dto2json(self, data):
        task_schema = TaskSchema(many=True)
        return task_schema.dump(data)

    def get_personal_tasks(
        self,
        current_user: dict,
        _from: int,
        size: int,
        start_date: str,
        end_date: str,
        counting: bool,
    ):
        start_date = convert_str2time(start_date)
        end_date = convert_str2time(end_date)
        # only allowing get current user tasks
        conditions = [
            Task.created_at >= start_date,
            Task.created_at <= end_date,
            Task.assignee == current_user.get("username"),
        ]
        sort_fields = parse_sort_query(Task, "-created_at")
        tasks, count = self.task_repo.search_tasks(
            _from, size, conditions, sort_fields, counting
        )

        return self.__dump_dto2json(tasks), count

    def __convert_query2filter(self, query):
        filters = []
        for k, v in query.items():
            if hasattr(Task, k):
                filters.append(getattr(Task, k) == v)
        return filters

    def get_all_tasks(
        self,
        _from: int,
        size: int,
        start_date: str,
        end_date: str,
        query: dict,
        sorts: str,
        counting: bool,
    ):
        """
        sorts: "-created_at,due_date"
        query: {
            "assignee": "kiennt96",
            "status_id": 4 (completed)
        }
        """
        sorted_fields = parse_sort_query(Task, sorts)
        start_date = convert_str2time(start_date)
        end_date = convert_str2time(end_date)

        filter_by = [Task.created_at >= start_date, Task.created_at <= end_date]
        filter_by += self.__convert_query2filter(query)
        tasks, count = self.task_repo.search_tasks(
            _from, size, filter_by, sorted_fields, counting
        )

        return self.__dump_dto2json(tasks), count

    def update_assigned_task_only(self, current_user, task_id, status_id):
        tasks, _ = self.task_repo.search_tasks(
            0,
            1,
            [Task.assignee == current_user.get("username"), Task.id == task_id],
            [],
            False,
        )
        if not tasks:
            raise Forbidden("Cannot update this task")
        task = tasks[0]
        if not self.workflow_service.is_valid_transition(
            task.task_type.workflow_id, task.status_id, status_id, current_user
        ):
            raise InvalidParameter(
                error_code=4001003, params="status_id", message="transition failed"
            )
        return self.task_repo.update_task(task_id, {"status_id": status_id})

    def update_task_by_manager(self, task_id: str, data: dict):
        return self.task_repo.update_task(task_id, data)

    def create_task(self, task_info):
        # do some validation on task here
        fields = list(task_info.keys())
        for field in fields:
            if not hasattr(Task, field):
                del task_info[field]
        # find the first status in the workflow and update task status
        task_info["status_id"] = 1
        return self.task_repo.create_task(task_info)

    def view_employee_task_report(
        self, _from: int, size: int, query, start_date: str, end_date: str, sort: str
    ):
        filter_by = [
            Task.created_at >= convert_str2time(start_date),
            Task.created_at <= convert_str2time(end_date),
        ]
        filter_by += self.__convert_query2filter(query)
        sorted_fields = parse_sort_query(Task, sort)
        data = self.task_repo.get_employee_task_summary(
            _from, size, filter_by, sorted_fields
        )

        return [list(employee_summary) for employee_summary in data]
