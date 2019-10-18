from datetime import datetime
import ebedke.utils.text

days_lower = ["hétfő", "kedd", "szerda", "csütörtök", "péntek", "szombat", "vasárnap"]
days_lower_ascii = ["hetfo", "kedd", "szerda", "csutortok", "pentek", "szombat", "vasarnap"]

months_hu_lower = ["január", "február", "március",
                   "április", "május", "június",
                   "július", "augusztus", "szeptember",
                   "október", "november", "december"]


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
