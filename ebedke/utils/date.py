from datetime import datetime
import ebedke.utils.text

days_lower = ["hétfő", "kedd", "szerda", "csütörtök", "péntek", "szombat", "vasárnap"]
days_lower_ascii = ["hetfo", "kedd", "szerda", "csutortok", "pentek", "szombat", "vasarnap"]
days_upper = [day.upper() for day in days_lower]

months_hu_lower = ["január", "február", "március",
                   "április", "május", "június",
                   "július", "augusztus", "szeptember",
                   "október", "november", "december"]

months_hu_capitalized = [month.capitalize() for month in months_hu_lower]



def parse_hungarian_month(month):
    month = ebedke.utils.text.remove_accents(month).lower()
    months = {
        "januar": 1,
        "februar": 2,
        "marcius": 3,
        "aprilis": 4,
        "majus": 5,
        "junius": 6,
        "julius": 7,
        "augusztus": 8,
        "szeptember": 9,
        "oktober": 10,
        "november": 11,
        "december": 12
    }
    if month in months:
        return months[month]
    else:
        return datetime.now().month

def workday(date):
    datestr = date.strftime("%Y-%m-%d")
    extra_workdays = [
        "2020-08-29", "2019-12-12"
    ]

    if datestr in extra_workdays:
        return True

    holidays = [
        "2019-12-25", "2019-12-26", "2019-12-27", "2020-01-01", "2020-04-10",
        "2020-05-01", "2020-06-01", "2020-08-20", "2020-08-21", "2020-10-23",
        "2020-12-24", "2020-12-25", "2020-12-26", "2021-01-01"
    ]

    if datestr in holidays:
        return False

    return date.weekday() < 5

def on_workdays(func):
    def wrapper(*args, **kwargs):
        if not workday(args[0]):
            return []
        else:
            return func(*args, **kwargs)
    return wrapper
