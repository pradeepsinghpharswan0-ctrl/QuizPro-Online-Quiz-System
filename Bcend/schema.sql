CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    question TEXT NOT NULL,
    optA TEXT NOT NULL,
    optB TEXT NOT NULL,
    optC TEXT NOT NULL,
    optD TEXT NOT NULL,
    correct TEXT NOT NULL,
    explanation TEXT
);

CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    score INTEGER NOT NULL,
    total INTEGER NOT NULL,
    category TEXT,
    difficulty TEXT,
    created_at TEXT
);