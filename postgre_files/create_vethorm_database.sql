CREATE TABLE servers(
    id BIGINT PRIMARY KEY,
    watch_mode BOOLEAN
);

CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    guild_id BIGINT REFERENCES servers(id),
    watching BOOLEAN
);

CREATE TABLE channels (
    id BIGINT PRIMARY KEY,
    guild_id BIGINT REFERENCES servers(id),
    watching BOOLEAN
);

CREATE TABLE user_logs (
    aid BIGINT PRIMARY KEY AUTO_INCREMENT,
    message_id BIGINT,
    user_id BIGINT REFERENCES users(id),
    guild_id BIGINT REFERENCES servers(id),
    message VARCHAR(2000),
    mtype VARCHAR(100),
    date TIMESTAMP
);

DROP TABLE user_logs

CREATE TABLE channel_logs (
    message_id BIGINT PRIMARY KEY,
    channel_id BIGINT REFERENCES channels(id),
    guild_id BIGINT REFERENCES servers(id),
    message VARCHAR(2000),
    mtype VARCHAR(100),
    date TIMESTAMP
);

CREATE TABLE tags (
    tag VARCHAR(128) PRIMARY KEY,
    guild_id BIGINT REFERENCES servers(id),
    info VARCHAR(2000)
);

CREATE TABLE watchlist (
    guild_id BIGINT REFERENCES servers(id),
    user_id BIGINT REFERENCES users(id),
    PRIMARY KEY (guild_id, user_id)
);

CREATE TABLE catalogue_alias (
    course_id VARCHAR(1024) PRIMARY KEY,
    guild_id BIGINT REFERENCES servers(id),
    alias VARCHAR(1024)
);