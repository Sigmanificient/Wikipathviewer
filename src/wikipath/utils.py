import re
from typing import List, Set
from urllib.parse import unquote

WIKI_LINKS_PATTERN = re.compile(
    "(?:(?:en[.]wikipedia[.]org)|[\"\'])"
    "(?:\\/wiki\\/([^\"\':?#]+)\")"
)

def parse_links(raw_content: str) -> List[str]:
    return re.findall(WIKI_LINKS_PATTERN, raw_content)


def clean_up_names(raw_names: List[str]) -> Set[str]:
    return {unquote(name) for name in raw_names}