# app/routers/embeddings.py
from fastapi import APIRouter, File, UploadFile, HTTPException
from app.face_recognition import FaceRecognizer
from app.database import get_db
from app import crud
import cv2
import numpy as np
from typing import List

router = APIRouter()
recognizer = FaceRecognizer()

@router.post("/embeddings/extract/{person_id}")
async def extract_embeddings(person_id: int, file: UploadFile = File(...)):
    """
    استخراج embeddings از تصویر و ذخیره برای person
    """
    try:
        # خواندن تصویر
        contents = await file.read()
        nparr = np.frombuffer(contents, dtype=np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # تشخیص چهره‌ها
        faces = recognizer.detect_faces(image)
        
        if len(faces) == 0:
            raise HTTPException(status_code=400, detail="No face detected in image")
        
        # استخراج embeddings
        embeddings: List[np.ndarray] = []
        for face_location in faces:
            embedding = recognizer.extract_embedding(image, face_location)
            embeddings.append(embedding)
            
            # ذخیره در دیتابیس
            with get_db() as db:
                crud.create_face_embedding(
                    db,
                    person_id=person_id,
                    embedding=embedding.tobytes()
                )
        
        # آموزش مدل
        recognizer.train(person_id, embeddings)
        
        return {
            "person_id": person_id,
            "faces_detected": len(faces),
            "embeddings_extracted": len(embeddings)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/embeddings/recognize")
async def recognize_face(file: UploadFile = File(...)):
    """
    تشخیص چهره در تصویر
    """
    try:
        # خواندن تصویر
        contents = await file.read()
        nparr = np.frombuffer(contents, dtype=np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # تشخیص چهره‌ها
        faces = recognizer.detect_faces(image)
        
        if len(faces) == 0:
            raise HTTPException(status_code=400, detail="No face detected in image")
        
        # تشخیص هر چهره
        results = []
        for face_location in faces:
            embedding = recognizer.extract_embedding(image, face_location)
            person_id = recognizer.recognize(embedding)
            
            if person_id is not None:
                with get_db() as db:
                    person = crud.get_person(db, person_id)
                
                results.append({
                    "person_id": person_id,
                    "name": person["name"] if person else "Unknown",
                    "location": face_location
                })
            else:
                results.append({
                    "person_id": None,
                    "name": "Unknown",
                    "location": face_location
                })
        
        return {"faces": results}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
