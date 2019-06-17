from typing import List, Iterable
import unicodedata

from ebedke.utils.date import days_lower_ascii

def normalize_menu(menu: Iterable[str]) -> List[str]:
    text = '\n'.join(line.strip() for line in menu)
    if len(text.strip()) < 16:
        return []
    if any(word in text.lower() for word in ("zárva", "ünnep", "nincs menü", "feltöltés")):
        return []
    if len(text) > 2000:
        text = text[0:2000]

    # remove emojis, "So" -> Symbol, other
    # https://en.wikipedia.org/wiki/Template:General_Category_(Unicode)
    emoji = lambda char: unicodedata.category(char) in ["So", "Cn", "Sk", "Cf"]
    text = ''.join(char for char in text if not emoji(char))

    lines = []
    for line in text.splitlines():
        line = line.strip()
        if len(line) > 2 and mostly_contains_letters(line) and not just_dayname(line):
            line = capitalize_if_shouting(line)
            lines.append(line)

    return remove_duplicates(lines)

def remove_duplicates(lines: List[str]) -> List[str]:
    return sorted(set(lines), key=lines.index)


def just_dayname(text: str) -> bool:
    for day in days_lower_ascii:
        if day in remove_accents(text.lower()) and len(text) <= len(day) + 4:
            return True
    return False


def mostly_contains_letters(text: str) -> bool:
    letters = sum(1 for c in text if c.isalpha())
    return letters / len(text) > 0.5

def capitalize_if_shouting(text: str) -> str:
    capitals = sum(1 for c in text if c.isupper())
    if capitals / len(text) > 0.6:
        return text.capitalize()
    else:
        return text

def skip_empty_lines(text, dropwords=()):
    for line in text:
        line = line.strip()
        if len(line) > 1 and not any(word in line for word in dropwords):
            yield line

def remove_accents(text):
    accentless = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("ascii")
    return accentless
