import psycopg2


def get_connection():
    return psycopg2.connect(
        dbname="task_scheduler_db",
        user="postgres",
        password="cos101",
        host="localhost",
        port="5432"
    )
