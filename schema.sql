CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    points INTEGER NOT NULL
);

CREATE TABLE points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    point_text TEXT,
    justification TEXT
);

ALTER TABLE points ADD COLUMN value NOT NULL default 0;
ALTER TABLE points RENAME TO transactions;