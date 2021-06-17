import os
from sqlalchemy import create_engine
from sqlalchemy.sql import text

engine = create_engine(os.environ.get("DATABASE_URI", ""))


def get_column_for_row(column_name, table_name, filter_column, value):
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT {} FROM {} WHERE {} = '{}'".format(
                column_name, table_name, filter_column, value
                )
            )
        )
        row = result.fetchone()
    
    return row[column_name] if row else None


def update_last_pulled_time_for_user(username, timestamp):
    data = {"timestamp": timestamp, "username": username}
    query = text("UPDATE users SET last_pulled_at=:timestamp WHERE username = :username")
    with engine.connect() as connection:
        connection.execute(query, **data)


def write_tweets_to_db(tweets, username):
    user_id = get_column_for_row("id", "users", "username", username)
    query = text("INSERT INTO tweets (tweet_id, tweet_text, created_at, twitter_user) VALUES (:id, :tweet, :created_at, :twitter_user)")
    with engine.connect() as connection:
        for tweet in tweets:
            tweet.update({"twitter_user": user_id})
            connection.execute(query, **tweet)


def initialize_user(username, timestamp):
    query = text("INSERT INTO users (username, last_pulled_at) VALUES (:username, :now)")
    data = {"username": username, "now": timestamp}
    with engine.connect() as connection:
        connection.execute(query, **data)


def update_tweets_pulled_for_user(username, count):
    current_tweets_pulled = get_column_for_row("tweets_pulled", "users", "username", username)
    data = {
        "count": current_tweets_pulled + count,
        "username": username,
    }
    query = text("UPDATE users SET tweets_pulled=:count WHERE username = :username")
    with engine.connect() as connection:
        connection.execute(query, **data)


def update_is_completed_status(username, status=True):
    data = {
        "status": status,
        "username": username,
    }
    query = text("UPDATE users SET is_completed=:status WHERE username = :username")
    with engine.connect() as connection:
        connection.execute(query, **data)


def search_tweets(search_term, username):
    if not search_term:
        return []
    user_id = get_column_for_row("id", "users", "username", username)
    results = []
    search_term = ' & '.join(search_term.split())

    query = """
    WITH user_tweets AS (
        SELECT tweet_text, tweet_tsv, created_at FROM tweets WHERE twitter_user = {}
    )
    SELECT tweet_text, created_at FROM user_tweets
    WHERE tweet_tsv @@ to_tsquery('{}')
    """.format(user_id, search_term)

    with engine.connect() as connection:
        rows = connection.execute(query)

    for row in rows:
        results.append({
            "tweet": row["tweet_text"],
            "created_at": row["created_at"]
        })

    return results


def get_tweets_of_user(username):
    user_id = get_column_for_row("id", "users", "username", username)
    results = []
    query = "SELECT tweet_id, tweet_text, created_at FROM tweets WHERE twitter_user = {}".format(user_id)

    with engine.connect() as connection:
        rows = connection.execute(query)

    for row in rows:
        results.append({
            "id": row["tweet_id"],
            "tweet": row["tweet_text"],
            "created_at": row["created_at"]
        })

    return results


def filter_tweets(start_date, end_date, chronological,username):
    results = []
    data = {
        "start_date": start_date,
        "end_date": end_date,
        "user_id": get_column_for_row("id", "users", "username", username)
    }
    query = """
    WITH user_tweets AS (
        SELECT tweet_text, created_at FROM tweets WHERE twitter_user = :user_id
    )
    SELECT tweet_text, created_at FROM user_tweets
    WHERE created_at BETWEEN :start_date and :end_date ORDER BY "tweet_text" {}
    """.format("ASC" if chronological else "DESC")

    with engine.connect() as connection:
        rows = connection.execute(text(query), data)

    for row in rows:
        results.append({
            "tweet": row["tweet_text"],
            "created_at": row["created_at"]
        })

    return results
