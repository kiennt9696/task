from datetime import datetime

import jwt


def get_current_user(token, public_key: str) -> str:
    token = jwt.decode(
        token, public_key.encode(), algorithms="RS256", options={"verify_aud": False}
    )
    return token


def parse_sort_query(model, sort_query: str):
    sort_criteria_list = list()
    field_name_list = sort_query.split(",")
    for field_name in field_name_list:
        if field_name is None:
            return None

        if field_name.startswith("-"):
            _field_name = field_name[1:]
            descending = True
        else:
            _field_name = field_name
            descending = False

        _field = getattr(model, _field_name, None)
        if _field is not None:
            if descending:
                sort_criteria_list.append(_field.desc())
            else:
                sort_criteria_list.append(_field)
    return sort_criteria_list


def convert_str2time(time_str: str):
    return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
