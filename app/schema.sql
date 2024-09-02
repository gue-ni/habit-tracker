
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_name TEXT NOT NULL,
  event_tag TEXT,
  event_type TEXT CHECK(event_type IN ('HABIT', 'QUIT', 'MEASURE')) NOT NULL DEFAULT 'HABIT',
  event_repeat TEXT CHECK(event_repeat IN ('DAILY', 'WEEKLY')) NOT NULL DEFAULT 'DAILY',
  event_repeat_per_week INTEGER CHECK (NOT (event_repeat = 'WEEKLY' AND event_repeat_per_week IS NULL)),
  event_emoji TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  user_id INTEGER,
  description TEXT,
  hex_color TEXT DEFAULT '#FF5733',
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS occurences (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id INTEGER,
  occured_at DATE DEFAULT CURRENT_DATE,
  comment TEXT,
  numeric_value FLOAT,
  UNIQUE (event_id, occured_at),
  FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS streaks (
  event_id INTEGER PRIMARY KEY,
  streak INTEGER NOT NULL DEFAULT 1,
  last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  active_since TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);
