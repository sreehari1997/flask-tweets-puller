import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["TWITTER_OAUTH_CLIENT_KEY"] = os.environ.get("API_KEY")
app.config["TWITTER_OAUTH_CLIENT_SECRET"] = os.environ.get("API_SECRET")
twitter_bp = make_twitter_blueprint()
app.register_blueprint(twitter_bp, url_prefix="/login")

@app.route("/")
def index():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    resp = twitter.get("account/verify_credentials.json")
    print(resp)
    assert resp.ok
    return "You are @{screen_name} on Twitter".format(screen_name=resp.json()["screen_name"])


@app.route('/hello')
def hello():
    if not twitter.authorized:
        print("not authorised")
    else:
        print("Authorised")
    return "Hello World!"
  
  
if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 5000, debug = True)