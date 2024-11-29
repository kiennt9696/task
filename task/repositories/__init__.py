from task.extension import db
from task.repositories.task import TaskRepository
from task.repositories.workflow import WorkflowRepository

task_repo = TaskRepository(db)
workflow_repo = WorkflowRepository(db=db)
