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