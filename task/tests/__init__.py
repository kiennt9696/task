# Create a base test class for shared setup
import unittest

from flask import Flask, request

from task.controllers.task import get_personal_tasks, get_all_tasks, update_assigned_task_only, assign_task_by_manager, \
    create_task, get_employee_task_summary


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the Flask app for testing
        self.app = Flask(__name__)
        self.app.testing = True
        self.client = self.app.test_client()

        # Register routes for testing with uniquely named view functions
        def personal_tasks_view():
            return get_personal_tasks(request.json)

        def all_tasks_view():
            return get_all_tasks(request.json)

        def update_task_view(task_id):
            return update_assigned_task_only(task_id, request.json)

        def assign_task_view():
            return assign_task_by_manager(request.json)

        def create_task_view():
            return create_task(request.json)

        def employee_summary_view():
            return get_employee_task_summary(request.json)

        self.app.add_url_rule(
            "/tasks/personal", view_func=personal_tasks_view, methods=["POST"]
        )
        self.app.add_url_rule(
            "/tasks/all", view_func=all_tasks_view, methods=["POST"]
        )
        self.app.add_url_rule(
            "/tasks/<task_id>/update", view_func=update_task_view, methods=["POST"]
        )
        self.app.add_url_rule(
            "/tasks/assign", view_func=assign_task_view, methods=["POST"]
        )
        self.app.add_url_rule(
            "/tasks/create", view_func=create_task_view, methods=["POST"]
        )
        self.app.add_url_rule(
            "/tasks/employee-summary", view_func=employee_summary_view, methods=["POST"]
        )

