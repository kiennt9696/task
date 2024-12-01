from flask import make_response


def options_handler():
    response = make_response()
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.status_code = 204
    return response


def own_task_options_handler():
    return options_handler()


def all_task_options_handler():
    return options_handler()
