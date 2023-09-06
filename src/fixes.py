import re

CLOZE_RE = re.compile(r"(?si)({{c\d+::)(.*)(}})")
HTML_RE = re.compile(r"<.*?>")

# https://developer.mozilla.org/en-US/docs/Glossary/Void_element
VOID_ELEMENTS = (
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
)


def fix_clozes_with_overlapping_html(text: str) -> str:
    def repl(match: re.Match) -> str:
        text = match.group(2)
        # Handle nested clozes
        text = fix_clozes_with_overlapping_html(text)
        new_start = 0
        before_cloze = ""
        opening_tags_count = 0
        for m in HTML_RE.finditer("".join(text)):
            tag = m.group()
            tag_name = tag.replace("<", "").replace(">", "").replace("/", "")
            if tag_name not in VOID_ELEMENTS:
                if not tag.startswith("</"):
                    opening_tags_count += 1
                elif opening_tags_count > 0:
                    opening_tags_count -= 1
                else:
                    before_cloze = text[: m.end()]
                    new_start = m.end()

        return before_cloze + match.group(1) + text[new_start:] + match.group(3)

    return CLOZE_RE.sub(repl, text)


def apply_all_fixes(text: str) -> str:
    return fix_clozes_with_overlapping_html(text)
