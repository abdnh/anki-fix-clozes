import re

# CLOZE_WITH_OVERLAPPING_HTML_RE = re.compile(r"(?si)({{c\d+::)((\</.*?\>)+)(.*?}})")
CLOZE_RE = re.compile(r"(?si)({{c\d+::)(.*?)(}})")
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
        new_start = 0
        new_end = len(text)
        before_cloze = ""
        after_cloze = ""
        opening_tags_count = 0
        matches = list(HTML_RE.finditer("".join(text)))
        for i, m in enumerate(matches):
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
            if opening_tags_count and i == len(matches) - 1:
                # Opening tag at the end of the cloze body
                after_cloze = text[m.start() :]
                new_end = m.start()

        return (
            before_cloze
            + match.group(1)
            + text[new_start:new_end]
            + match.group(3)
            + after_cloze
        )

    return CLOZE_RE.sub(repl, text)


def apply_all_fixes(text: str) -> str:
    return fix_clozes_with_overlapping_html(text)
