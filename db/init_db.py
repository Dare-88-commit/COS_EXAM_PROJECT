import psycopg2
from db.connection import get_connection


def init_db():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Create table only if it doesn't exist (preserves existing data)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    priority TEXT CHECK (priority IN ('Low', 'Medium', 'High')),
                    deadline TIMESTAMP,
                    completed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("Database initialized successfully!")
    except Exception as e:
        print(f"Database initialization error: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
