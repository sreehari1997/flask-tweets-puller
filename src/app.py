from config import Config
from flask import Flask, redirect, url_for
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter

app = Flask(__name__)
app.config.from_object(Config)
twitter_bp = make_twitter_blueprint()
app.register_blueprint(twitter_bp, url_prefix="/login")

@app.route("/")
def index():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    response = twitter.get("account/verify_credentials.json")
    assert response.ok
    twitter_username = response.json()["screen_name"]
    return "Welcome @{}".format(twitter_username)
  
  
if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 5000, debug = True)