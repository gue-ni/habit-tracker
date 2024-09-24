from datetime import datetime, date


def datestring_to_obj(string):
    return datetime.strptime(string, "%Y-%m-%d").date()


def obj_to_datestring(obj):
    return obj.strftime("%Y-%m-%d")


def get_current_date():
    today = date.today()
    return obj_to_datestring(today)
