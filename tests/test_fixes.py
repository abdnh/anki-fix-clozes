from src.fixes import fix_clozes_with_overlapping_html


def test_fixes_clozes_with_overlapping_single_tag() -> None:
    text = "hello <span>world {{c1::</span>test}}"
    expected = "hello <span>world </span>{{c1::test}}"
    replaced = fix_clozes_with_overlapping_html(text)
    assert replaced == expected


def test_fixes_clozes_with_multiple_overlapping_tags() -> None:
    text = "hello <span><b>world {{c1::</b></span>test}}"
    expected = "hello <span><b>world </b></span>{{c1::test}}"
    replaced = fix_clozes_with_overlapping_html(text)
    assert replaced == expected
