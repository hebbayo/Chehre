# app/crud.py
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, List, Dict, Any

# Person CRUD
def create_person(conn: psycopg2.extensions.connection, name: str) -> Optional[Dict[str, Any]]:
    """ایجاد person جدید"""
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO persons (name) VALUES (%s) RETURNING id, name, created_at",
                (name,)
            )
            result = cur.fetchone()
            conn.commit()
            return dict(result) if result else None
    except Exception as e:
        conn.rollback()
        raise e


def get_person(conn: psycopg2.extensions.connection, person_id: int) -> Optional[Dict[str, Any]]:
    """دریافت person با ID"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT id, name, created_at FROM persons WHERE id = %s",
            (person_id,)
        )
        result = cur.fetchone()
        return dict(result) if result else None


def get_all_persons(conn: psycopg2.extensions.connection) -> List[Dict[str, Any]]:
    """دریافت تمام persons"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id, name, created_at FROM persons ORDER BY created_at DESC")
        results = cur.fetchall()
        return [dict(row) for row in results]


def delete_person(conn: psycopg2.extensions.connection, person_id: int) -> bool:
    """حذف person"""
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM persons WHERE id = %s", (person_id,))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e


# Face Image CRUD
def create_face_image(
    conn: psycopg2.extensions.connection,
    person_id: int,
    image_data: bytes
) -> Optional[Dict[str, Any]]:
    """ذخیره تصویر چهره"""
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO face_images (person_id, image_data) VALUES (%s, %s) RETURNING id, person_id, created_at",
                (person_id, psycopg2.Binary(image_data))
            )
            result = cur.fetchone()
            conn.commit()
            return dict(result) if result else None
    except Exception as e:
        conn.rollback()
        raise e


def get_face_image_by_id(conn: psycopg2.extensions.connection, face_id: int) -> Optional[Dict[str, Any]]:
    """دریافت تصویر چهره با ID"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT id, person_id, created_at FROM face_images WHERE id = %s",
            (face_id,)
        )
        result = cur.fetchone()
        return dict(result) if result else None


def get_faces_by_person(conn: psycopg2.extensions.connection, person_id: int) -> List[Dict[str, Any]]:
    """دریافت تمام تصاویر چهره یک person"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT id, person_id, created_at FROM face_images WHERE person_id = %s ORDER BY created_at DESC",
            (person_id,)
        )
        results = cur.fetchall()
        return [dict(row) for row in results]


def delete_face(conn: psycopg2.extensions.connection, face_id: int) -> bool:
    """حذف تصویر چهره"""
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM face_images WHERE id = %s", (face_id,))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e


# Face Embedding CRUD
def create_face_embedding(
    conn: psycopg2.extensions.connection,
    person_id: int,
    embedding: bytes
) -> Optional[Dict[str, Any]]:
    """ذخیره embedding چهره"""
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO face_embeddings (person_id, embedding) VALUES (%s, %s) RETURNING id, person_id, created_at",
                (person_id, psycopg2.Binary(embedding))
            )
            result = cur.fetchone()
            conn.commit()
            return dict(result) if result else None
    except Exception as e:
        conn.rollback()
        raise e


def get_face_embedding(conn: psycopg2.extensions.connection, embedding_id: int) -> Optional[Dict[str, Any]]:
    """دریافت embedding با ID"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT id, person_id, embedding, created_at FROM face_embeddings WHERE id = %s",
            (embedding_id,)
        )
        result = cur.fetchone()
        return dict(result) if result else None


def get_all_face_embeddings(conn: psycopg2.extensions.connection) -> List[Dict[str, Any]]:
    """دریافت تمام embeddings"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id, person_id, embedding, created_at FROM face_embeddings")
        results = cur.fetchall()
        return [dict(row) for row in results]


def get_person_embeddings(conn: psycopg2.extensions.connection, person_id: int) -> List[Dict[str, Any]]:
    """دریافت embeddings یک person"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT id, person_id, embedding, created_at FROM face_embeddings WHERE person_id = %s",
            (person_id,)
        )
        results = cur.fetchall()
        return [dict(row) for row in results]


def update_face_embedding(
    conn: psycopg2.extensions.connection,
    embedding_id: int,
    embedding: bytes
) -> bool:
    """بروزرسانی embedding"""
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE face_embeddings SET embedding = %s WHERE id = %s",
                (psycopg2.Binary(embedding), embedding_id)
            )
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e


def delete_face_embedding(conn: psycopg2.extensions.connection, embedding_id: int) -> bool:
    """حذف embedding"""
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM face_embeddings WHERE id = %s", (embedding_id,))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e
