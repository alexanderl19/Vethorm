CREATE TABLE guilds (
    guild_id BIGINT PRIMARY KEY,
    -- TODO: currently flag for all users + channels, switch to separate flags
    watch_mode BOOLEAN
);

CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    guild_id BIGINT REFERENCES guilds(guild_id)
);

CREATE TABLE channels (
    chan_id BIGINT PRIMARY KEY,
    guild_id BIGINT REFERENCES guilds(guild_id),
    watching BOOLEAN
);

CREATE TABLE user_logs (
    -- u_log_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    message_id BIGINT,
    user_id BIGINT REFERENCES users(user_id),
    guild_id BIGINT REFERENCES guilds(guild_id),
    msg VARCHAR(2000),
    msg_type VARCHAR(100),
    msg_date TIMESTAMP
);

CREATE TABLE channel_logs (
    -- c_log_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    message_id BIGINT,
    user_id BIGINT REFERENCES users(user_id),
    channel_id BIGINT REFERENCES channels(chan_id),
    guild_id BIGINT REFERENCES guilds(guild_id),
    msg VARCHAR(2000),
    msg_type VARCHAR(100),
    msg_date TIMESTAMP
);

CREATE TABLE tags (
    tag VARCHAR(128) PRIMARY KEY,
    guild_id BIGINT REFERENCES guilds(guild_id),
    info VARCHAR(2000)
);

CREATE TABLE catalogue_alias (
    -- Currently only allows one alias
    department VARCHAR(1024) PRIMARY KEY,
    guild_id BIGINT REFERENCES guilds(guild_id),
    alias VARCHAR(1024)
);