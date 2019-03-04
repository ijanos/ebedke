
def normalize_menu(menu):
    text = '\n'.join(line.strip() for line in menu)
    if len(text.strip()) < 16:
        return []
    if any(word in text.lower() for word in ("zárva", "ünnep", "nincs menü")):
        return []
    if len(text) > 2000:
        text = text[0:2000]
    # remove emojis
    text = ''.join(char for char in text if ord(char) < 500)
    return text.splitlines()

def skip_empty_lines(text):
    for line in text:
        line = line.strip()
        if len(line) > 1:
            yield line
