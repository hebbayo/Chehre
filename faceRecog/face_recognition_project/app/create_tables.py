import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # جدول persons
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # جدول face_images
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS face_images (
            id SERIAL PRIMARY KEY,
            person_id INTEGER REFERENCES persons(id) ON DELETE CASCADE,
            image_path VARCHAR(500) NOT NULL,
            embedding BYTEA NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ جداول با موفقیت ساخته شدند")

if __name__ == "__main__":
    create_tables()
