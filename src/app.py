from config import Config
from flask import Flask, redirect, url_for, jsonify
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from twitter_utils import get_timeline_for_user
from flask_sqlalchemy import SQLAlchemy
from db_utils import (
    get_user_id,
    update_last_pulled_time_for_user,
    get_last_pulled_time_for_user,
    write_tweets_to_db,datetime,
    initialize_user,
    update_tweets_pulled_for_user
)
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
twitter_bp = make_twitter_blueprint()
app.register_blueprint(twitter_bp, url_prefix="/login")
db = SQLAlchemy(app)

@app.route("/")
def index():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    resp = twitter.get("account/verify_credentials.json")
    assert resp.ok
    twitter_username = resp.json()["screen_name"]
    user_id = get_user_id(db.engine, twitter_username)
    last_pulled_at = get_last_pulled_time_for_user(db.engine, twitter_username)
    if user_id:
        update_last_pulled_time_for_user(db.engine, twitter_username, datetime.utcnow())
    else:
        initialize_user(db.engine, twitter_username, datetime.utcnow())

    timeline, count = get_timeline_for_user(twitter_username, last_pulled_at)
    update_tweets_pulled_for_user(db.engine, twitter_username, count)
    write_tweets_to_db(db.engine, timeline, twitter_username)
    return jsonify({"success": True})

@app.route("/check")
def db_check():
    users = db.engine.execute("select username from users")
    for user in users:
        print(user)
    return "db check"

  
  
if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 5000, debug = True)
