from datetime import datetime
from sqlalchemy.sql import (
    text
)


def get_user_id(engine, username):
    with engine.connect() as connection:
        result = connection.execute(
            text("select id from users where username = '{}'".format(username))
        )
        
        for row in result:
            try:
                return row["id"]
            except KeyError:
                return None


def get_tweets_pulled_for_user(engine, username):
    with engine.connect() as connection:
        result = connection.execute(
            text("select tweets_pulled from users where username = '{}'".format(username))
        )
        
        for row in result:
            try:
                return row["tweets_pulled"]
            except KeyError:
                return None


def get_last_pulled_time_for_user(engine, username):
    with engine.connect() as connection:
        result = connection.execute(
            text("select last_pulled_at from users where username = '{}'".format(username))
        )
        
        for row in result:
            try:
                return row["last_pulled_at"]
            except KeyError:
                return None

    return


def update_last_pulled_time_for_user(engine, username, timestamp):
    data = {"timestamp": timestamp, "username": username}
    query = text("update users set last_pulled_at=:timestamp where username = :username")
    with engine.connect() as connection:
        connection.execute(query, **data)


def write_tweets_to_db(engine, tweets, username):
    user_id = get_user_id(engine, username)
    query = text("INSERT INTO tweets (tweet_id, tweet_text, created_at, twitter_user) VALUES (:id, :tweet, :created_at, :twitter_user)")
    with engine.connect() as connection:
        for tweet in tweets:
            tweet.update({"twitter_user": user_id})
            connection.execute(query, **tweet)


def initialize_user(engine, username, timestamp):
    query = text("INSERT INTO users (username, last_pulled_at) VALUES (:username, :now)")
    data = {"username": username, "now": timestamp}
    with engine.connect() as connection:
        connection.execute(query, **data)


def update_tweets_pulled_for_user(engine, username, count):
    current_tweets_pulled = get_tweets_pulled_for_user(engine, username)
    data = {
        "count": current_tweets_pulled + count,
        "username": username,
    }
    query = text("update users set tweets_pulled=:count where username = :username")
    with engine.connect() as connection:
        connection.execute(query, **data)
