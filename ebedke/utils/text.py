from typing import List, Iterable, Callable
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

    # https://en.wikipedia.org/wiki/Template:General_Category_(Unicode)
    not_emoji = lambda char: unicodedata.category(char) in ["Lu", "Ll", "Lt", "Lm", "Lo", "Zs", "Cc", "Nd", "Po", "Pe", "Pd", "Ps", "Sm"]
    text = ''.join(char for char in text if not_emoji(char))

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

def skip_empty_lines(text: List[str], dropwords: Iterable[str] = ()) -> List[str]:
    ret = []
    for line in text:
        line = line.strip()
        if len(line) > 1 and not any(word in line.lower() for word in dropwords):
            ret.append(line)
    return ret

def remove_accents(text: str) -> str:
    accentless = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("ascii")
    return accentless

def pattern_slice(
        iterator: Iterable[str],
        start_patterns: List[str],
        end_patterns: List[str],
        inclusive: bool = False,
        modifier: Callable[[str], str] = str.lower
    ) -> List[str]:
    if not isinstance(iterator, list):
        iterator = list(iterator)
    start = [len(iterator)]
    end = []
    for i, line in enumerate(iterator):
        if any(p in modifier(line) for p in start_patterns):
            start.append(i if inclusive else i + 1)
        elif any(p in modifier(line) for p in end_patterns):
            end.append(i)
    start_index = start.pop()
    end_index = next((x for x in end if x >= start_index), len(iterator))
    return iterator[start_index:end_index]
