from config import Config
from flask import Flask, redirect, url_for, jsonify
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from twitter_utils import get_timeline_for_user
from flask_sqlalchemy import SQLAlchemy

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
    timeline = get_timeline_for_user(twitter_username)
    return jsonify(timeline)

@app.route("/check")
def db_check():
    users = db.engine.execute("select username from users")
    for user in users:
        print(user)
    return "db check"

  
  
if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 5000, debug = True)
