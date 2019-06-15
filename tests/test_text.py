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

def test_normalize():
    menu = ["", "\n\n\n", "\t\t\t\taa\t\n", "test menu"]
    assert text.normalize_menu(menu) == [], "Too short texts should be dropped"
    menu.append("   this is a longer test text\t\n")
    assert text.normalize_menu(menu) == ["test menu", "this is a longer test text"]
    closed_menu = ["sajnos ma zárva vagyunk"]
    assert text.normalize_menu(closed_menu) == []
    menu = [" test test 1 ", "1234Ft", "test test 2   ", "aa!#!!aa"]
    assert text.normalize_menu(menu) == ["test test 1", "test test 2"]

def test_no_duplicates():
    menu = ["line 1", "line 2", "line 2"]
    assert text.normalize_menu(menu) == ["line 1", "line 2"]
    menu = ["line 1", "    line 2", "line 2   "]
    assert text.normalize_menu(menu) == ["line 1", "line 2"]
    menu = ["line 1", "line 2", "line 3", "line 2"]
    assert text.normalize_menu(menu) == ["line 1", "line 2", "line 3"]
