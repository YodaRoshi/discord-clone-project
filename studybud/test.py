import pytz
from datetime import datetime, timezone

utc=pytz.UTC

from dateutil.relativedelta import relativedelta
from django.utils.timesince import TIME_STRINGS as timesince_time_strings
from django.utils.html import avoid_wrapping
from django.utils.translation import gettext, get_language
import inflect 
p = inflect.engine()

    
def timesince():
    test = datetime(2026, 6, 30, 8, 3, 2, 345784, tzinfo=timezone.utc)
    test2 = datetime(2023, 7, 1, 10, 2, 1, 345784, tzinfo=timezone.utc)
    delta = relativedelta(test, test2)

    # delta = relativedelta(now, d)
    years = delta.years
    months = delta.months
    weeks = delta.days // 7
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
    
str = timesince()

print(str)
