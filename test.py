from datetime import datetime, timedelta

def get_last_five_weeks_dates():
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())

    days = []

    for i in range(5):
        week_start = start_of_week - timedelta(weeks=i)
        week_dates = [week_start + timedelta(days=d) for d in range(7)]
        days += week_dates

    return days

# Get the dates
last_five_weeks_dates = get_last_five_weeks_dates()

print(len(last_five_weeks_dates))

print(last_five_weeks_dates)
