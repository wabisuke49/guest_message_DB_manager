CREATE TABLE IF NOT EXISTS messages (
    message_id TEXT PRIMARY KEY NOT NULL,
    received_at TEXT NOT NULL,
    session_id TEXT NOT NULL,
    house_id TEXT NOT NULL,
    guest_message TEXT NOT NULL
);
