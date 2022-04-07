
CREATE TABLE IF NOT EXISTS devices (
    /*  Store mac_address as an int, convert it before/after passing.
        Needs to be 6 bytes, so BIGINT covvers us. */
    mac_address BIGINT UNSIGNED NOT NULL UNIQUE PRIMARY KEY,
    mac_string CHAR(17),
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivered_date TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    days_active INT UNSIGNED,
    times_flashed INT UNSIGNED,
    lines_of_code INT UNSIGNED,
    logins INT UNSIGNED,
    pings INT UNSIGNED,
    label CHAR(4),
    cohort CHAR(4)
);

CREATE TABLE IF NOT EXISTS moods (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    mood_name CHAR(8) NOT NULL UNIQUE,
    mood_count INT UNSIGNED
);

CREATE TABLE IF NOT EXISTS params (
    paramName VARCHAR(50) NOT NULL,
    paramValue VARCHAR(100)
);

INSERT INTO params (paramName, paramValue) VALUES ('current_mood', 'HAPPY');
