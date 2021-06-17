import os
from datetime import datetime
from .db_utils import (
    get_column_for_row,
    update_last_pulled_time_for_user,
    initialize_user,
    update_tweets_pulled_for_user,
    write_tweets_to_db,
    update_is_completed_status
)

from .twitter_utils import get_timeline_for_user


def pull_tweets_of_user(username):
    user_id = get_column_for_row("id", "users", "username", username)
    last_pulled_at = get_column_for_row("last_pulled_at", "users", "username", username)
    if user_id:
        update_last_pulled_time_for_user(username, datetime.utcnow())
    else:
        initialize_user(username, datetime.utcnow())

    timeline, count = get_timeline_for_user(username, last_pulled_at)
    write_tweets_to_db(timeline, username)
    update_tweets_pulled_for_user(username, count)
    update_is_completed_status(username)


def pull_new_tweets_of_users():
    ## get all the usernames in the platform
    users = []
    for user in users:
        pull_tweets_of_user()