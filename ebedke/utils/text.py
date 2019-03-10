from unicodedata import category

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
    text = ''.join(char for char in text if not category(char).startswith("So"))

    lines = []
    for line in text.splitlines():
        line = line.strip()
        if len(line) > 2:
            lines.append(line)

    return lines

def skip_empty_lines(text):
    for line in text:
        line = line.strip()
        if len(line) > 1:
            yield line
