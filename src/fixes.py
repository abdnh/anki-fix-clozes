import re

CLOZE_WITH_OVERLAPPING_HTML_RE = re.compile(r"(?si)({{c\d+::)((\</.*?\>)+)(.*?}})")


def fix_clozes_with_overlapping_html(text: str) -> str:
    def repl(match: re.Match) -> str:
        return match.group(2) + match.group(1) + match.group(4)

    return CLOZE_WITH_OVERLAPPING_HTML_RE.sub(repl, text)


def apply_all_fixes(text: str) -> str:
    return fix_clozes_with_overlapping_html(text)
