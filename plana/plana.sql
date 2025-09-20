--
-- File generated with SQLiteStudio v3.4.17 on Пт сен 19 18:31:36 2025
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: Notifications
CREATE TABLE IF NOT EXISTS Notifications (id INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL, description TEXT, begin_date DATE NOT NULL, begin_time TIME NOT NULL, deadline_date DATE NOT NULL, deadline_time TIME NOT NULL, completion BOOL);
INSERT INTO Notifications (id, name, description, begin_date, begin_time, deadline_date, deadline_time, completion) VALUES (1, 'попить', 'воды', '01.01.2025', '0:00', '01.01.2026', '23:59', NULL);
INSERT INTO Notifications (id, name, description, begin_date, begin_time, deadline_date, deadline_time, completion) VALUES (2, 'dasdasdsa', '', '18.09.2025', '19:56', '18.09.2025', '23:59', NULL);
INSERT INTO Notifications (id, name, description, begin_date, begin_time, deadline_date, deadline_time, completion) VALUES (3, 'asdasdas', '', '18.09.2025', '19:57', '18.09.2025', '23:59', NULL);
INSERT INTO Notifications (id, name, description, begin_date, begin_time, deadline_date, deadline_time, completion) VALUES (4, 'd', '', '18.09.2025', '20:06', '18.09.2025', '23:59', NULL);
INSERT INTO Notifications (id, name, description, begin_date, begin_time, deadline_date, deadline_time, completion) VALUES (5, 'dasdasdas', '', '18.09.2025', '20:06', '18.09.2025', '23:59', NULL);
INSERT INTO Notifications (id, name, description, begin_date, begin_time, deadline_date, deadline_time, completion) VALUES (6, 'dddd', '', '19.09.2025', '11:28', '19.09.2025', '23:59', NULL);

-- Table: Notifications_periods
CREATE TABLE IF NOT EXISTS Notifications_periods (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, id_notifications INTEGER REFERENCES Notifications (id), id_periods INTEGER REFERENCES Periods (id));
INSERT INTO Notifications_periods (id, id_notifications, id_periods) VALUES (1, 1, 1);

-- Table: Periods
CREATE TABLE IF NOT EXISTS Periods (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, name TEXT NOT NULL, delta INTEGER NOT NULL);
INSERT INTO Periods (id, name, delta) VALUES (1, 'year', 1);

-- Table: processed_sessions
CREATE TABLE IF NOT EXISTS processed_sessions (session_id TEXT PRIMARY KEY);

-- Table: sessions
CREATE TABLE IF NOT EXISTS sessions (session_id TEXT PRIMARY KEY, user_id TEXT REFERENCES users (user_id), token TEXT, created INTEGER, authorized INTEGER DEFAULT (0));

-- Table: users
CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, username TEXT, first_name TEXT, last_name TEXT, session_id TEXT);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
