from flask import request, jsonify, current_app

from helpers.util import get_current_user
from task.services import task_service

PUBLIC_KEY = "PUBLIC_KEY"


def __get_search_basic_params(body):
    _from = body.get("_from", 0)
    size = body.get("size", 100)
    start_date = body.get("start_date")
    end_date = body.get("end_date")
    counting = body.get("counting")
    query = body.get("query", {})
    sort = body.get("sort", "")
    return _from, size, start_date, end_date, counting, query, sort


def get_personal_tasks(body):
    _from, size, start_date, end_date, counting, _, sort = __get_search_basic_params(
        body
    )
    current_user = get_current_user(
        request.authorization.token, current_app.config.get(PUBLIC_KEY)
    )
    tasks, count = task_service.get_personal_tasks(
        current_user, _from, size, start_date, end_date, counting
    )
    return jsonify({"tasks": tasks, "count": count}), 200


def get_all_tasks(body):
    _from, size, start_date, end_date, counting, query, sort = (
        __get_search_basic_params(body)
    )
    tasks, count = task_service.get_all_tasks(
        _from, size, start_date, end_date, query, sort, counting
    )
    return jsonify({"tasks": tasks, "count": count}), 200


def update_assigned_task_only(task_id, body):
    current_user = get_current_user(
        request.authorization.token, current_app.config.get(PUBLIC_KEY)
    )
    task_service.update_assigned_task_only(current_user, task_id, body.get("status_id"))
    return jsonify(), 204


def assign_task_by_manager(body):
    task_id = body.get("task_id")
    del body["task_id"]
    task_service.update_task_by_manager(task_id, body)
    return jsonify(), 204


def create_task(body):
    task = task_service.create_task(body)
    return jsonify({"task_id": task.id}), 200


def get_employee_task_summary(body):
    _from, size, start_date, end_date, _, query, sort = __get_search_basic_params(body)
    data = task_service.view_employee_task_report(
        _from, size, query, start_date, end_date, sort
    )
    return jsonify({"report": data}), 200
