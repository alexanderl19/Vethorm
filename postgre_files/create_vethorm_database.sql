CREATE TABLE IF NOT EXISTS guilds (
    guild_id BIGINT PRIMARY KEY,
    -- TODO: currently flag for all users + channels, switch to separate flags
    watch_mode BOOLEAN
);

CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    guild_id BIGINT REFERENCES guilds(guild_id)
);

CREATE TABLE IF NOT EXISTS channels (
    chan_id BIGINT PRIMARY KEY,
    guild_id BIGINT REFERENCES guilds(guild_id),
    watching BOOLEAN
);

CREATE TABLE IF NOT EXISTS voice_channels (
    voice_id BIGINT PRIMARY KEY,
    text_id BIGINT,
    guild_id BIGINT REFERENCES guilds(guild_id),
    role_id BIGINT
);

CREATE TABLE IF NOT EXISTS user_logs (
    -- u_log_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    message_id BIGINT,
    user_id BIGINT REFERENCES users(user_id),
    guild_id BIGINT REFERENCES guilds(guild_id),
    msg VARCHAR(2000),
    msg_type VARCHAR(100),
    msg_date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS channel_logs (
    -- c_log_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    message_id BIGINT,
    user_id BIGINT REFERENCES users(user_id),
    channel_id BIGINT REFERENCES channels(chan_id),
    guild_id BIGINT REFERENCES guilds(guild_id),
    msg VARCHAR(2000),
    msg_type VARCHAR(100),
    msg_date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tags (
    tag VARCHAR(128) PRIMARY KEY,
    guild_id BIGINT REFERENCES guilds(guild_id),
    info VARCHAR(2000)
);

CREATE TABLE IF NOT EXISTS catalogue_alias (
    -- Currently only allows one alias
    department VARCHAR(1024) PRIMARY KEY,
    guild_id BIGINT REFERENCES guilds(guild_id),
    alias VARCHAR(1024)
);