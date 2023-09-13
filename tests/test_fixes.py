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


def test_fixes_clozes_overlapping_element_after_valid_ones() -> None:
    text = "<div>{{c5::<strong><br></strong></div><div><strong></strong></div>test}}"
    expected = (
        "<div><strong><br></strong></div>{{c5::<div><strong></strong></div>test}}"
    )
    replaced = fix_clozes_with_overlapping_html(text)
    assert replaced == expected


def test_fixes_clozes_with_opening_tag_at_end() -> None:
    text = "{{c1::test<div>zz}}ww</div>"
    expected = "{{c1::test}}<div>zzww</div>"
    replaced = fix_clozes_with_overlapping_html(text)
    assert replaced == expected
