import os
import tweepy


def create_tweepy_client():
    auth = tweepy.OAuthHandler(
        os.environ.get("TWITTER_API_KEY", ""),
        os.environ.get("TWITTER_API_SECRET", "")
    )
    auth.set_access_token(
        os.environ.get("TWITTER_ACCESS_TOKEN", ""),
        os.environ.get("TWITTER_ACCESS_SECRET", "")
    )

    client = tweepy.API(auth)
    return client


def get_timeline(client, screen_name):
    timeline = []
    for status in tweepy.Cursor(client.user_timeline, id=screen_name).items():
        timeline.append({
            "id": status.id,
            "tweet_text": status.text,
            "created_at": status.created_at
        })

    return timeline


def get_timeline_for_user(screen_name):
    client = create_tweepy_client()
    timeline = get_timeline(client, screen_name)
    return timeline
