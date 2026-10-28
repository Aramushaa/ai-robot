import sqlite3

def init_db(db_path="robot.db"):
    connection = sqlite3.connect(db_path)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS robot_commands (
            id INTEGER PRIMARY KEY,
            command TEXT NOT NULL,
            status_before TEXT NOT NULL,
            status_after TEXT NOT NULL,
            http_status_code INTEGER NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

    print("Database initialized successfully!")


def save_command(command, status_before, status_after, http_status_code,db_path="robot.db"):
    connection = sqlite3.connect(db_path)

    connection.execute(
    """
    INSERT INTO robot_commands
    (command, status_before, status_after, http_status_code)
    VALUES (?, ?, ?, ?)
    """,
    (command, status_before, status_after, http_status_code)
    )

    connection.commit()
    connection.close()


def get_command_history(db_path="robot.db"):
    connection = sqlite3.connect(db_path)
    rows = connection.execute(
        """
        SELECT id, command, status_before, status_after,
               http_status_code, created_at
        FROM robot_commands
        ORDER BY id DESC
        """
    ).fetchall()
    connection.close()
    return rows



