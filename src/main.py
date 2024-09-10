from fastapi import FastAPI
from datetime import date
import uvicorn

from schemas import Repo, CommitActivity, order_options
from db import get_top_100_repos, get_commit_activity
from settings import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)


@app.get("/api/repos/top100", response_model=list[Repo])
async def top_100_repos(order_by: order_options):
    """Топ 100 репозиторий на гите по кол-ву звезд."""
    return get_top_100_repos(order_by)


@app.get("/api/repos/{owner}/{repo:path}/activity", response_model=list[CommitActivity])
async def repo_activity(owner: str, repo: str, since: date, until: date):
    """Since и until должны быть в формате YYYY-MM-DD."""
    return get_commit_activity(owner, repo, since, until)


if __name__ == "__main__":
    uvicorn.run(app=app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
