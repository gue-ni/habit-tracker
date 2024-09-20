
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
  longest_streak INTEGER NOT NULL DEFAULT 1,
  last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  active_since TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS quotes;

CREATE TABLE IF NOT EXISTS quotes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  quote TEXT NOT NULL,
  author TEXT NOT NULL
);

INSERT INTO quotes (quote, author) VALUES
  ('Habits change into character.', 'Ovid'),
  ('Good habits formed at youth make all the difference.', 'Aristotle'),
  ('Successful people are simply those with successful habits.', 'Brian Tracy'),
  ("Rome wasn't built in a day.", 'Unknown'),
  ("There is no elevator to success, you have to take the stairs.", "Zig Ziglar"),
  ("Our life is what our thoughts make it.", "Marcus Aurelius"),
  ("Each day provides its own gifts.", "Marcus Aurelius"),
  ("We become what we repeatedly do.", "Sean Covey"),
  ("A nail is driven out by another nail; habit is overcome by habit.", "Erasmus"),
  ("Habit is a cable; we weave a thread of it each day, and at last, we cannot break it.", "Horace Mann"),
  ("A man should be upright, not be kept upright.", "Marcus Aurelius");