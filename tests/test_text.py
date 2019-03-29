from ebedke.utils import text

def test_remove_accents():
    hetfo = "hétfő"
    HETFO = "HÉTFŐ"
    assert text.remove_accents(hetfo) == "hetfo"
    assert text.remove_accents(HETFO) == "HETFO"

def test_remove_emojis():
    text_with_emojies = ["some 🤜🏻🍗🍔🥓🍟", "text 🔜👨🏼‍🍳 here"]
    normalized = text.normalize_menu(text_with_emojies)
    assert normalized == ["some", "text  here"]