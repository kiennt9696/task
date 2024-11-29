from task.repositories import task_repo, workflow_repo
from task.services.task import TaskService
from task.services.workflow import WorkflowService

workflow_service = WorkflowService(workflow_repo)
task_service = TaskService(task_repo=task_repo, workflow_service=workflow_service)
