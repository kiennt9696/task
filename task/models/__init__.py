from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    Integer,
    Text,
    create_engine,
)
from datetime import datetime

from sqlalchemy.orm import relationship

Base = declarative_base()


class AuditTable(Base):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    updated_by = Column(String, nullable=True)


class Task(AuditTable):
    __tablename__ = "task"

    id = Column(String, primary_key=True)
    title = Column(String)
    description = Column(String)
    creator = Column(String)
    parent_id = Column(String, ForeignKey("task.id"))
    type_id = Column(Integer, ForeignKey("task_type.id"))
    status_id = Column(Integer, ForeignKey("task_status.id"))
    severity_id = Column(Integer, ForeignKey("task_severity.id"))
    assignee = Column(String)
    due_date = Column(DateTime, nullable=True)

    parent = relationship("Task", backref="children", remote_side=[id])
    task_type = relationship("TaskType")
    task_status = relationship("TaskStatus")
    task_severity = relationship("TaskSeverity")


class TaskType(Base):
    __tablename__ = "task_type"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    workflow_id = Column(Integer, ForeignKey("workflow.id"))

    workflow = relationship("Workflow")


class TaskSeverity(Base):
    __tablename__ = "task_severity"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class TaskStatus(Base):
    __tablename__ = "task_status"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Workflow(Base):
    __tablename__ = "workflow"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


class Transition(Base):
    __tablename__ = "transition"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    from_status_id = Column(Integer, ForeignKey("task_status.id"))
    to_status_id = Column(Integer, ForeignKey("task_status.id"))
    workflow_id = Column(Integer, ForeignKey("workflow.id"))
    resolution = Column(String)
    comment = Column(Text)
    requires_approval = Column(Boolean)
    approver = Column(String)

    from_status = relationship("TaskStatus", foreign_keys=[from_status_id])
    to_status = relationship("TaskStatus", foreign_keys=[to_status_id])
    workflow = relationship("Workflow")


class User(Base):
    __tablename__ = "user"
    id = Column(String, primary_key=True)
    username = Column(String)
    role = Column(String)
    firstname = Column(String)
    lastname = Column(String)


if __name__ == "__main__":
    db_uri = "postgresql+psycopg2://postgres:postgres@127.0.0.1:8432/task_management?application_name=task_management"
    engine = create_engine(db_uri)
    Base.metadata.create_all(engine)
