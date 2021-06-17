from .config import Config
from .proxy import ReverseProxied
from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from .db_utils import (
    search_tweets,
    get_tweets_of_user,
    get_column_for_row,
    filter_tweets
)
from .forms import FilterForm, SearchForm

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)
app.config.from_object(Config)
twitter_bp = make_twitter_blueprint()
app.register_blueprint(twitter_bp, url_prefix="/login")


@app.route("/", methods=['GET','POST'])
def index():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    resp = twitter.get("account/verify_credentials.json")
    assert resp.ok
    twitter_username = resp.json()["screen_name"]

    form = SearchForm()
    if form.validate_on_submit():
        search_terms = form.search.data
        tweets = search_tweets(search_terms, twitter_username)
    else:
        tweets = get_tweets_of_user(twitter_username)

    context = {
        "username": twitter_username,
        "tweets_pulled": get_column_for_row("tweets_pulled", "users", "username", twitter_username),
        "last_updated_at": get_column_for_row("last_pulled_at", "users", "username", twitter_username)
    }
    return render_template('index.html', context=context, form=form, tweets=tweets)


@app.route("/filter", methods=['GET','POST'])
def filter():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    resp = twitter.get("account/verify_credentials.json")
    assert resp.ok
    twitter_username = resp.json()["screen_name"]

    form = FilterForm()
    if form.validate_on_submit():
        print("viola")
        start_date = form.startdate.data
        end_date = form.enddate.data
        chronological = form.chronological.data
        tweets = filter_tweets(
            start_date, end_date, chronological, twitter_username
        )
    else:
        tweets = get_tweets_of_user(twitter_username)

    context = {
        "username": twitter_username
    }
    return render_template('filter.html', context=context, form=form, tweets=tweets)

@app.route("/check")
def check():
    return "check"
