from dataclasses import dataclass, astuple
from datetime import date, timedelta

from api import get_stars_data, get_repo_activity
from db import update_top_100, save_daily_repo_activity


@dataclass(slots=True)
class InsertData:
    repo: str
    owner: str
    position_cur: int
    stars: int
    watchers: int
    forks: int
    open_issues: int
    language: str


@dataclass(slots=True)
class CommitInsertData:
    date: date
    commits: int
    authors: list[str]
    repo_id: int


def prepare_repo_data(d: dict, ind: int) -> tuple:
    """Подготовить данные для записи в repo."""
    return astuple(
        InsertData(
            repo=d["full_name"],
            owner=d["owner"]["login"],
            position_cur=ind + 1,
            stars=d["stargazers_count"],
            watchers=d["watchers_count"],
            forks=d["forks_count"],
            open_issues=d["open_issues_count"],
            language=d["language"],
        )
    )


def prepare_activity_data(d_list: list[dict], repo_id: int) -> tuple:
    """Подготовить данные для записи в repo_activity."""
    authors = [d["author"]["login"] for d in d_list if d["author"]]
    return astuple(
        CommitInsertData(
            date=date.today() - timedelta(1),
            commits=len(d_list),
            authors=authors,
            repo_id=repo_id,
        )
    )


def main(event, context):
    data_list = get_stars_data()
    assert len(data_list) == 100
    for i, repo_data in enumerate(data_list):
        repo_id = update_top_100(prepare_repo_data(repo_data, i))
        activity_data = get_repo_activity(repo_data["commits_url"])

        if not activity_data:
            continue
        save_daily_repo_activity(prepare_activity_data(activity_data, repo_id))


if __name__ == "__main__":
    main()
