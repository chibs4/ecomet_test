from dotenv import load_dotenv
import psycopg
import os

load_dotenv()

conn_params = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_SERVER", "localhost"),
    "port": os.getenv("POSTGRESS_PORT", "5432"),
}

update_query = """
    INSERT INTO repos (repo, owner, position_cur, stars, watchers, forks, open_issues, language)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (repo, owner)
    DO UPDATE SET
        position_prev = repos.position_cur,
        position_cur = EXCLUDED.position_cur,
        stars = EXCLUDED.stars,
        watchers = EXCLUDED.watchers,
        forks = EXCLUDED.forks,
        open_issues = EXCLUDED.open_issues,
        language = EXCLUDED.language
    RETURNING id;
"""


def update_top_100(data: list[tuple]) -> int:
    """Обновить данные по топ 100 репо. Возвращает id из бд."""
    with psycopg.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute(update_query, data)
            return cur.fetchone()[0]  # id


def save_daily_repo_activity(data: tuple):
    insert_query = """
    INSERT INTO repo_activity (date, commits, authors, repo_id)
    VALUES (%s, %s, %s, %s);
    """
    with psycopg.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute(insert_query, data)
    pass
