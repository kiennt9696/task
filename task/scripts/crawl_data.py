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

    # Fetch data from tables
    data = {
        "task_type": [r.__dict__ for r in session.query(TaskType).all()],
        "task_severity": [p.__dict__ for p in session.query(TaskSeverity).all()],
        "task_status": [p.__dict__ for p in session.query(TaskStatus).all()],
        "workflow": [p.__dict__ for p in session.query(Workflow).all()],
        "transition": [s.__dict__ for s in session.query(Transition).all()],
        "task": [s.__dict__ for s in session.query(Task).all()],
        "user": [s.__dict__ for s in session.query(User).all()],
    }

    # Remove SQLAlchemy metadata fields like _sa_instance_state
    for table in data.values():
        for row in table:
            row.pop("_sa_instance_state", None)
            row.pop("updated_at", None)
            row.pop("created_at", None)

    # Save to JSON file
    with open("workflow_base_data.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Base data exported to workflow_base_data.json")
