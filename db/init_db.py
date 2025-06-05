from db.connection import get_connection


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Drop existing table if it exists
        cur.execute("DROP TABLE IF EXISTS tasks")

        # Create new table with updated schema
        cur.execute("""
            CREATE TABLE tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                priority TEXT,
                deadline DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                duration INTEGER
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    init_db()
