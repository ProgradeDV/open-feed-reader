"""functions for converting links related to a feed to the feed url"""
from urllib.parse import urlparse
import re
import requests
from bs4 import BeautifulSoup


def convert_youtube_channel(url:str) -> str:
    """find the rss feed link for a given youtube channel"""
    parsed_url = urlparse(url)

    assert parsed_url.netloc == 'www.youtube.com'
    assert re.match(r"^/@\w+$", parsed_url.path) # mathces "/@{channelname_name}"

    # pull the url
    page = requests.get(url, timeout=5)
    soup = BeautifulSoup(page.content)
    link = soup.find(title='RSS')
    return link['href']


def convert_bluesky_account(url:str) -> str:
    """find the rss link for a given bluesky account"""
    parsed_url = urlparse(url)

    assert parsed_url.netloc == 'bsky.app'
    assert re.match(r"^/profile/\w+\.\w+\.\w+$", parsed_url.path) # mathces "/profile/{profile_name}"

    new_path = parsed_url.path + '/rss'

    return parsed_url._replace(path=new_path).geturl()


def convert_subreddit(url:str) -> str:
    """find the rss link for a given subredit"""
    parsed_url = urlparse(url)

    assert parsed_url.netloc == 'www.reddit.com'
    assert re.match(r"^/r/\w+/$", parsed_url.path) # mathces "/r/{subreddit_name}/"

    new_path = parsed_url.path[:-1] + '.rss'

    return parsed_url._replace(path=new_path).geturl()
