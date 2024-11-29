CREATE INDEX idx_task_assignee ON Task(assignee);
CREATE INDEX idx_task_status_id ON Task(status_id);
CREATE INDEX idx_user_username ON User(username);
CREATE INDEX idx_user_role ON User(role);

CREATE INDEX idx_task_compound ON Task(assignee, status_id);