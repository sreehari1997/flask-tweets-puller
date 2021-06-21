## Flask app to fetch, search, filter tweets from twitter

Built using
- docker
- flask
- postgres
- sqlalchemy
- gunicorn
- nginx

### Features

- User sign in with twitter (flask dance : https://flask-dance.readthedocs.io/en/latest/)
- Application fetches users twitter timeline and save it to database
- UI will display the tweets in chronological order from db
- Sort & filter based on date on db
- Ability to search tweets on db

### Architecture
![alt text](https://github.com/sreehari1997/flask-tweets-puller/blob/master/architecture.png?raw=true)

### Database

DDL of tables, indices and triggers

```SQL
-- users Table Definition ----------------------------------------------

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username character varying(100) NOT NULL UNIQUE,
    job_id integer,
    is_completed boolean NOT NULL DEFAULT false,
    tweets_pulled integer DEFAULT 0,
    last_pulled_at timestamp without time zone
);

-- Indices -------------------------------------------------------

CREATE UNIQUE INDEX IF NOT EXISTS users_pkey ON users(id int4_ops);
CREATE UNIQUE INDEX IF NOT EXISTS users_username_key ON users(username text_ops);

-- tweets Table Definition ----------------------------------------------

CREATE TABLE IF NOT EXISTS tweets (
    tweet_id bigint PRIMARY KEY,
    tweet_text text,
    tweet_tsv tsvector,
    created_at timestamp without time zone,
    twitter_user integer REFERENCES users(id) ON DELETE CASCADE
);

-- Indices -------------------------------------------------------

CREATE UNIQUE INDEX IF NOT EXISTS tweets_pkey ON tweets(tweet_id int8_ops);
CREATE TRIGGER tsvupdate BEFORE INSERT or UPDATE on tweets FOR EACH ROW EXECUTE PROCEDURE tsvector_update_trigger (
    tweet_tsv, 'pg_catalog.english', tweet_text
);

CREATE INDEX IF NOT EXISTS ts_ix ON tweets USING GIN (tweet_tsv);
```

### How to run this app

Make sure that you've docker and docker-compose in your machine
```bash
git clone https://github.com/sreehari1997/flask-tweets-puller.git
```
```bash
cd flask-tweets-puller
```
```bash
docker-compose up --build
```

viola the application is up, go to ```http://127.0.0.1/```

### Working

- Twitter oAuth authentication is done using flask dance, first user is directed to twitter for auth and when the user is authenticated by twitter the user is redirected to the app.
- If the user is visiting the app for the first time, we will fetch all the tweets of user, when the same user is logged into the app next time, all the tweets from his timeline is not fetched only new tweets of the user is fetched from twitter.
- Postgres full text search: For searching the tweets of the user I've used full text search capability of postgres.
- When a new tweet is fetched from twitter and inserted or updated into tweets table ```tsvupdate``` trigger is triggered and a procedure ```tsvector_update_trigger``` is executed, which will create text space vector of that tweets and save into ```tweet_tsv``` column.
- (example)tweet : How does it feel to hear your songs on the radio!
- text space vector of the above tweet : 'feel':4 'hear':6 'radio':11 'song':8
- During searching the search terms (songs radio) are compared against the tweet_tsv ```SELECT tweet_text FROM tweets WHERE tweet_tsv @@ to_tsquery('songs & radio')```
