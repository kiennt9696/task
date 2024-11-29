import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from task.models import (
    TaskType,
    TaskSeverity,
    TaskStatus,
    Workflow,
    Transition,
    Task,
    User,
)

if __name__ == "__main__":

    db_uri = "postgresql+psycopg2://postgres:postgres@127.0.0.1:8432/task_management?application_name=task"
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Load data from JSON file
    with open("workflow_base_data.json", "r") as f:
        data = json.load(f)

    # Insert data into tables
    for task_severity in data["task_severity"]:
        session.add(TaskSeverity(**task_severity))
        session.flush()

    for task_status in data["task_status"]:
        session.add(TaskStatus(**task_status))
        session.flush()

    for workflow in data["workflow"]:
        session.add(Workflow(**workflow))
        session.flush()

    for task_type in data["task_type"]:
        session.add(TaskType(**task_type))
        session.flush()

    for transition in data["transition"]:
        session.add(Transition(**transition))
        session.flush()

    for task in data.get("task", []):
        session.add(Task(**task))
        session.flush()

    for user in data.get("users", []):
        session.add(User(**user))
        session.flush()
    # Commit changes
    session.commit()

    print("Base data initialized in the new system")
