-- users Table Definition ----------------------------------------------

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username character varying(100) NOT NULL UNIQUE,
    job_id integer,
    is_completed boolean NOT NULL DEFAULT false,
    tweets_pulled integer DEFAULT 0,
    last_pulled_at timestamp without time zone
);

-- Indices -------------------------------------------------------

CREATE UNIQUE INDEX users_pkey ON users(id int4_ops);
CREATE UNIQUE INDEX users_username_key ON users(username text_ops);

-- tweets Table Definition ----------------------------------------------

CREATE TABLE tweets (
    tweet_id bigint PRIMARY KEY,
    tweet_text character varying(300),
    created_at timestamp without time zone,
    twitter_user integer REFERENCES users(id) ON DELETE CASCADE
);

-- Indices -------------------------------------------------------

CREATE UNIQUE INDEX tweets_pkey ON tweets(tweet_id int8_ops);