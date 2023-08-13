import re
from typing import List
from urllib.parse import unquote

WIKI_LINKS_PATTERN = re.compile(r'(?=en.wikipedia.org)|["]/wiki\/([^":?#]+)"')

def parse_links(raw_content: str) -> List[str]:
    return re.findall(WIKI_LINKS_PATTERN, raw_content)


def clean_up_names(raw_names: List[str]) -> List[str]:
    return [unquote(name) for name in raw_names]