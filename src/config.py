import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', "supersecret")
    TWITTER_OAUTH_CLIENT_KEY = os.environ.get("API_KEY", "")
    TWITTER_OAUTH_CLIENT_SECRET = os.environ.get("API_SECRET", "")