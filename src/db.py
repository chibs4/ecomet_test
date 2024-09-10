import psycopg
from psycopg.rows import dict_row
from datetime import date

from schemas import order_options
from settings import settings


def get_db_connection():
    """Can be used as context manager."""
    conn = psycopg.connect(str(settings.POSTGRES_URI), row_factory=dict_row)
    return conn


def get_top_100_repos(order_by: order_options) -> list[dict]:
    query = f"""
        SELECT repo, owner, position_cur, position_prev, stars, watchers, forks, open_issues, language
        FROM repos
        ORDER BY {order_by} DESC
        LIMIT 100;
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            repos = cur.fetchall()
            return repos


def get_commit_activity(owner: str, repo: str, since: date, until: date) -> list[dict]:
    query = """
        SELECT ra.date, ra.commits, ra.authors
        FROM repo_activity ra
        JOIN repos r ON ra.repo_id = r.id
        WHERE r.owner = %s AND r.repo = %s AND ra.date BETWEEN %s AND %s;
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (owner, repo, since, until))
            activity = cur.fetchall()
            return activity
