CREATE TABLE IF NOT EXISTS user(
	user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	guild_id CHAR(18) NOT NULL,
	user_name VARCHAR(20) NOT NULL,
	is_assignable BOOLEAN NOT NULL CHECK(is_assignable IN (0, 1))
);

CREATE TABLE IF NOT EXISTS ticket(
	ticket_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER NOT NULL,
	assigned_user_id INTEGER,
	ticket_title VARCHAR(50) NOT NULL,
	ticket_description TEXT NOT NULL,
	ticket_tag VARCHAR(20),
	is_closed BOOLEAN NOT NULL CHECK(is_closed IN (0, 1)),
	ticket_created_on DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY(user_id) REFERENCES user(user_id),
	FOREIGN KEY(assigned_user_id) REFERENCES user(user_id)
);

CREATE TABLE IF NOT EXISTS message(
	message_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	ticket_id INTEGER NOT NULL,
	user_id INTEGER NOT NULL,
	message_text TEXT NOT NULL,
	message_sent_on DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY(ticket_id) REFERENCES ticket(ticket_id),
	FOREIGN KEY(user_id) REFERENCES user(user_id)
);
