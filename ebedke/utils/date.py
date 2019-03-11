from utils.text import remove_accents


def parse_hungarian_month(month):
    month = remove_accents(month).lower()
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
        return None
