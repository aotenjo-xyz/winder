import sqlite3


def init_db():
    conn = sqlite3.connect("motors.db")
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS motors (
            motor_id INTEGER NOT NULL UNIQUE,
            target REAL NOT NULL,
            position REAL NOT NULL,
            updated_at TEXT DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'now'))
        )
    """
    )
    # Initialize motors
    for motor_id in range(4):
        cur.execute(
            """
            INSERT OR IGNORE INTO motors (motor_id, target, position, updated_at)
            VALUES (?, ?, ?, STRFTIME('%Y-%m-%d %H:%M:%f', 'now', 'localtime'))
        """,
            (motor_id, 0.0, 0.0),
        )

    conn.commit()
    return conn


def update_motor_target(conn, motor_id, target):
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE motors
        SET target = ?, updated_at = STRFTIME('%Y-%m-%d %H:%M:%f', 'now', 'localtime')
        WHERE motor_id = ?
    """,
        (target, motor_id),
    )
    conn.commit()


def update_motor_position(conn, motor_id, position):
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE motors
        SET position = ?, updated_at = STRFTIME('%Y-%m-%d %H:%M:%f', 'now', 'localtime')
        WHERE motor_id = ?
    """,
        (position, motor_id),
    )
    conn.commit()


def get_motor_data(conn, motor_id):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT motor_id, target, position, updated_at
        FROM motors
        WHERE motor_id = ?
    """,
        (motor_id,),
    )
    return cur.fetchone()


def get_all_motors(conn):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT motor_id, target, position, updated_at
        FROM motors
    """
    )
    return cur.fetchall()


def main():
    conn = init_db()

    # Fetch and print motor data
    for motor_id in range(4):
        data = get_motor_data(conn, motor_id)
        print(
            f"Motor {data[0]} - Target: {data[1]:.2f}, Position: {data[2]:.2f}, Updated At: {data[3]}"
        )

    conn.close()


if __name__ == "__main__":
    main()
