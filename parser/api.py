import requests
from datetime import datetime, timedelta

REPO_URL = "https://api.github.com/search/repositories"


def get_stars_data() -> list[dict]:
    """Получение отсортированного списка самых популярных репо из гита."""
    params = dict(q="stars:>1", sort="stars", per_page=100)
    resp = requests.get(REPO_URL, params=params)
    if resp.status_code != 200:
        raise ValueError("Error getting stars data from API")
    data = resp.json()
    return data["items"]


def get_repo_activity(url: str) -> list[dict]:
    """URl можно взять из поля commits_url. Берутся данные за вчерашний день."""

    def get_yesterday_start_and_end() -> tuple[str, str]:
        now = datetime.utcnow()
        yesterday_start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0)
        yesterday_end = (now - timedelta(days=1)).replace(hour=23, minute=59, second=59)
        yesterday_start_iso = yesterday_start.isoformat() + "Z"
        yesterday_end_iso = yesterday_end.isoformat() + "Z"
        return yesterday_start_iso, yesterday_end_iso

    url_without_suff = url.split("{")[0]
    since, until = get_yesterday_start_and_end()
    params = dict(since=since, until=until, per_page=100)
    resp = requests.get(url_without_suff, params=params)
    if resp.status_code != 200:
        print(resp.text)
        raise ValueError(f"Error getting data from {url_without_suff}")
    return resp.json()
