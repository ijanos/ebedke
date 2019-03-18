from unicodedata import category
from unicodedata import normalize

def normalize_menu(menu):
    text = '\n'.join(line.strip() for line in menu)
    if len(text.strip()) < 16:
        return []
    if any(word in text.lower() for word in ("zárva", "ünnep", "nincs menü")):
        return []
    if len(text) > 2000:
        text = text[0:2000]

    # remove emojis, "So" -> Symbol, other
    # https://en.wikipedia.org/wiki/Template:General_Category_(Unicode)
    emoji = lambda char: category(char) in ["So", "Cn"]
    text = ''.join(char for char in text if not emoji(char))

    lines = []
    for line in text.splitlines():
        line = line.strip()
        if len(line) > 2:
            line = capitalize_if_shouting(line)
            lines.append(line)

    return lines

def capitalize_if_shouting(text):
    capitals = sum(1 for c in text if c.isupper())
    if capitals / len(text) > 0.6:
        return text.capitalize()
    else:
        return text

def skip_empty_lines(text):
    for line in text:
        line = line.strip()
        if len(line) > 1:
            yield line

def remove_accents(text):
    accentless = normalize('NFD', text).encode('ascii', 'ignore').decode("ascii")
    return accentless