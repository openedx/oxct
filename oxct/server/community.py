import json
import os
import re
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from oxct.common.exceptions import OxctError, OxctNotFoundError

from .cache import memoize

DISCOURSE_URL = os.environ.get("OXCT_DISCOURSE_URL", "https://discuss.openedx.org")
DISCOURSE_API_TIMEOUT_SECONDS = int(
    os.environ.get("OXCT_DISCOURSE_API_TIMEOUT_SECONDS", 5)
)


class Member:
    def __init__(self, data):
        self._data = data
        self._api_user_data = None

    def as_dict(self):
        return {
            "name": self.name,
            "bio": {
                "html": self.bio_html,
                "txt": self.bio_txt,
            },
            "tags": self.tags,
            "username": self.username,
            "likes_received": self.likes_received,
        }

    @property
    def username(self):
        return self._data["user"]["username"]

    @property
    def id(self):
        return self._data["user"]["id"]

    @property
    def name(self):
        return self._data["user"]["name"]

    @property
    def likes_received(self):
        return self._data["likes_received"]

    @property
    def bio_html(self):
        # Note that the "bio_cooked" field may be absent or None.
        return self.api_user_data["user"].get("bio_cooked") or ""

    @property
    def bio_txt(self):
        return BeautifulSoup(self.bio_html, "html.parser").get_text()

    @property
    def tags(self):
        """
        Parse #tags from bio.
        """
        return parse_hashtags(self.bio_txt)

    @property
    def api_user_data(self):
        if self._api_user_data is None:
            self._api_user_data = get_json(f"/users/{self.username}.json")
        return self._api_user_data


def find_member(username):
    for member in iter_members():
        if member.username == username:
            return member
    raise OxctNotFoundError("Member could not be found")


def iter_members():
    for result in iter_paginated_json(
        "/directory_items.json",
        params={"period": "all", "order": "likes_received"},
        key="directory_items",
    ):
        yield Member(result)


@memoize
def list_tags():
    tags = set()
    for member in iter_members():
        tags.update(member.tags)
    return sorted(tags)


def iter_paginated_json(endpoint, params=None, key=None):
    # Surprisingly, discourse paging starts at page 0
    page = 0
    while True:
        params["page"] = page
        results = get_json(endpoint, params)
        if key:
            results = results[key]
        if not results:
            break
        yield from results
        page += 1


@memoize
def get_json(endpoint, params=None):
    url = DISCOURSE_URL + endpoint
    if params:
        url += "?" + urlencode(params)
    try:
        response = urlopen(Request(url), timeout=DISCOURSE_API_TIMEOUT_SECONDS)
    except HTTPError as e:
        raise OxctError(
            f"Discourse API: {e.code} HTTP error while trying to fetch {url}"
        ) from e
    # TODO handle timeout and deserialization errors
    return json.loads(response.read())


def parse_hashtags(text):
    """
    Parse "#xxx" hashtags from a text.
    """
    tags = set()
    for tag in re.findall(r"#(?P<tag>[a-zA-Z\.-_]+)", text):
        tags.add(tag.lower())
    return sorted(tags)
