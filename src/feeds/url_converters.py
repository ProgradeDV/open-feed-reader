"""Converting links related to a feed to the feed url."""
import re
from urllib.parse import ParseResult, parse_qs

import requests
from bs4 import BeautifulSoup

YOUTUBE_URL_REGEX = r"^/@\w+$" # mathces "/@{channelname_name}..."
BLUESKY_URL_REGEX = r"^/profile/\w+\.\w+\.\w+$" # mathces "/profile/{profile_name}"
REDDIT_URL_REGEX = r"^/r/\w+/$" # mathces "/r/{subreddit_name}/"


def get_rss_url(parsed_url:ParseResult) -> str:
    """Convert the given url into the corisponding rss url."""
    if parsed_url.netloc == "www.youtube.com":
        return convert_youtube_channel(parsed_url)

    if parsed_url.netloc == "bsky.app":
        return convert_bluesky_account(parsed_url)

    if parsed_url.netloc == "www.reddit.com":
        return convert_subreddit(parsed_url)

    return parsed_url.geturl()


def convert_youtube_channel(parsed_url:ParseResult) -> str:
    """Find the rss feed link for a given youtube channel."""
    if re.match(YOUTUBE_URL_REGEX, parsed_url.path): # mathces "/@{channelname_name}..."
        # remove any parameters
        parsed_url._replace(query="")  # noqa: SLF001

        # pull the url
        page = requests.get(parsed_url.geturl(), timeout=5)
        soup = BeautifulSoup(page.content, "html.parser")
        link = soup.find(title="RSS")
        return link["href"]

    if "list" in (query := parse_qs(parsed_url.query)):
        return f"https://www.youtube.com/feeds/videos.xml?playlist_id={query['list'][0]}"

    raise ValueError("Unreconized link")


def convert_bluesky_account(parsed_url:ParseResult) -> str:
    """Find the rss link for a given bluesky account."""
    if not re.match(BLUESKY_URL_REGEX, parsed_url.path):
        raise ValueError("Unreconized link")

    new_path = parsed_url.path + "/rss"

    return parsed_url._replace(path=new_path).geturl()  # noqa: SLF001


def convert_subreddit(parsed_url:ParseResult) -> str:
    """Find the rss link for a given subredit."""
    if not re.match(REDDIT_URL_REGEX, parsed_url.path):
        raise ValueError("Unreconized link")

    new_path = parsed_url.path[:-1] + ".rss"

    return parsed_url._replace(path=new_path).geturl()  # noqa: SLF001
