import rethinkdb as r
from tokenDB import token_query
from datetime import time, datetime, timedelta
import rt_server as rts

r.connect(rts.ip, rts.port, rts.db_name).repl()
lunch_event = {"alarm": False,
               "color": "#536DFE",
               "editable": False,
               "eventOverlap": False,
               "flexible_lunch": True
               }


def set_lunch(event):
    lunch_event["title"] = event["title"]

    lunch_event["range_max"] = event["range_max"]
    lunch_event["duration_event"] = event["duration_event"]

    #setting coord starting and meeting point
    lunch_event["starting_location"] = event["starting_location"]
    lunch_event["meeting_location"] = event["meeting_location"]

    # setting alarm message and timer
    lunch_event["alarm_timer"] = event["alarm_timer"]
    lunch_event["alarm_message"] = event["alarm_message"]

    # setting route
    lunch_event["route"] = event["route"]

    create_lunch(event)
    return ""


def create_lunch(event):
    email = token_query(event["token"])
    starting_time = datetime.strptime(event["range_min"], "%H:%M")
    starting_day = datetime.strptime(event["starting_flexible_day"], "%Y-%m-%d").\
        replace(hour=starting_time.hour, minute=starting_time.minute)
    ending_day = datetime.strptime(event["ending_flexible_day"], "%Y-%m-%d")
    for timestamp in datespan(starting_day, ending_day):
        start = timestamp
        end = start + timedelta(hours=datetime.strptime(event["duration_event"], "%H:%M").hour,
                                minutes=datetime.strptime(event["duration_event"], "%H:%M").minute)
        create_lunch_event(start, end, email)


def create_lunch_event(start, end, email):
    lunch_event["start"] = start.strftime("%Y-%m-%d %H:%M+00:00")
    lunch_event["end"] = end.strftime("%Y-%m-%d %H:%M+00:00")
    cursor = r.table("event").insert(lunch_event).run()
    id = cursor["generated_keys"][0]
    r.table("event_submit").insert({"event": id, "email": email}).run()


def rearrange_lunch(lunch, e):
    end_lunch_time = time(hour=datetime.strptime(lunch["range_max"], "%H:%M").hour,
                          minute=datetime.strptime(lunch["range_max"], "%H:%M").minute)
    new_end = datetime.strptime(e["end"], "%Y-%m-%d %H:%M+00:00") + \
        timedelta(hours=datetime.strptime(lunch["duration_event"], "%H:%M").hour,
                  minutes=datetime.strptime(lunch["duration_event"], "%H:%M").minute)
    new_end = new_end.strftime("%Y-%m-%d %H:%M+00:00")
    lunch_end = time(hour=datetime.strptime(new_end, "%Y-%m-%d %H:%M+00:00").hour,
                     minute=datetime.strptime(new_end, "%Y-%m-%d %H:%M+00:00").minute)
    if lunch_end > end_lunch_time:
        lunch["alarm"] = True
        r.table("event").get(lunch["id"]).update(lunch).run()
    else:
        lunch["start"] = e["end"]
        lunch["end"] = new_end
        r.table("event").get(lunch["id"]).update(lunch).run()


def datespan(start_date, end_date, delta=timedelta(days=1)):
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += delta
