from pydantic import BaseModel
from typing import Literal
from datetime import date


class Repo(BaseModel):
    repo: str
    owner: str
    position_cur: int
    position_prev: int
    stars: int
    watchers: int
    forks: int
    open_issues: int | None
    language: str | None

    @classmethod
    def field_names(cls) -> list[str]:
        return cls.__fields__.keys()


class CommitActivity(BaseModel):
    date: date
    commits: int
    authors: list[str]


order_options = Literal[*Repo.field_names()]
