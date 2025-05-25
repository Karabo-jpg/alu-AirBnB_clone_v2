USE hbnb_test_db;

CREATE TABLE IF NOT EXISTS states (
    id VARCHAR(60) PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    name VARCHAR(128) NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS cities (
    id VARCHAR(60) PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    state_id VARCHAR(60),
    name VARCHAR(128) NOT NULL DEFAULT '',
    FOREIGN KEY (state_id) REFERENCES states(id)
);

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(60) PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    email VARCHAR(128) NOT NULL DEFAULT '',
    password VARCHAR(128) NOT NULL DEFAULT '',
    first_name VARCHAR(128) DEFAULT '',
    last_name VARCHAR(128) DEFAULT ''
);

CREATE TABLE IF NOT EXISTS places (
    id VARCHAR(60) PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    city_id VARCHAR(60),
    user_id VARCHAR(60),
    name VARCHAR(128) NOT NULL DEFAULT '',
    description VARCHAR(1024),
    number_rooms INT NOT NULL DEFAULT 0,
    number_bathrooms INT NOT NULL DEFAULT 0,
    max_guest INT NOT NULL DEFAULT 0,
    price_by_night INT NOT NULL DEFAULT 0,
    latitude FLOAT,
    longitude FLOAT,
    FOREIGN KEY (city_id) REFERENCES cities(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS amenities (
    id VARCHAR(60) PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    name VARCHAR(128) NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS reviews (
    id VARCHAR(60) PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    place_id VARCHAR(60),
    user_id VARCHAR(60),
    text VARCHAR(1024) DEFAULT '',
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
