# app/database.py
import psycopg2
from contextlib import contextmanager

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/face_recognition"


@contextmanager
def get_db():
    """Context manager برای مدیریت اتصال به دیتابیس"""
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def get_db_connection():
    """ایجاد اتصال مستقیم به دیتابیس (برای استفاده در routerها)"""
    return psycopg2.connect(DATABASE_URL)


def init_db():
    """مقداردهی اولیه دیتابیس"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # جدول persons
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS persons (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # جدول faces
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS faces (
                id SERIAL PRIMARY KEY,
                person_id INTEGER NOT NULL,
                image_data BYTEA NOT NULL,
                embedding BYTEA,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE
            )
        """)
        
        conn.commit()
        print("Database initialized successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error initializing database: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
