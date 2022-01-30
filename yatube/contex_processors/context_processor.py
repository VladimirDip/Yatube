import datetime as dt


def year(request):
    now = dt.datetime.now().year
    return {"year": now}