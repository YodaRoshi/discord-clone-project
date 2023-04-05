from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import inflect 

p = inflect.engine()

def time_since(since):
    test = datetime(2026, 6, 30, 8, 3, 2, 345784, tzinfo=timezone.utc)
    test2 = datetime(2023, 7, 1, 10, 2, 1, 345784, tzinfo=timezone.utc)
    delta = relativedelta(test, test2)
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    delta = relativedelta(now, since)
    years = delta.years
    months = delta.months
    weeks = delta.weeks
    days = delta.days - weeks * 7
    hours = delta.hours
    minutes = delta.minutes

    if (years > 0):
        return str(years) + " " + p.plural("year", years)
    elif (months > 0):
        return str(months) + " " + p.plural("month", months)
    elif (weeks > 0):
        return str(weeks) + " " + p.plural("week", weeks)
    elif (days > 0):
        return str(days) + " " + p.plural("day", days)
    elif (hours > 0):
        return str(hours) + " " + p.plural("hour", days)
    else:
        return str(minutes)+ " " + p.plural("minute", days)
