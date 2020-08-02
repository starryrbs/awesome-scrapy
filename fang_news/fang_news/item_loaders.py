from dateutil.parser import parse
from w3lib.html import remove_tags, strip_html5_whitespace


def format_date(text: str):
    return parse(strip_html5_whitespace(text))


def filter_invalid_url(url: str):
    if isinstance(url, str):
        url = url.lower()
        if 'http' in url or 'https' in url:
            return url
