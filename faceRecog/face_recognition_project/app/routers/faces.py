# app/routers/faces.py
from fastapi import APIRouter, File, UploadFile, HTTPException
from app.database import get_db
from app import crud
import cv2
import numpy as np

router = APIRouter()

@router.post("/faces/{person_id}")
async def upload_face(person_id: int, file: UploadFile = File(...)):
    """
    آپلود تصویر چهره برای یک person
    """
    try:
        # بررسی وجود person
        with get_db() as db:
            person = crud.get_person(db, person_id)
            if person is None:
                raise HTTPException(status_code=404, detail="Person not found")
        
        # خواندن تصویر
        contents = await file.read()
        nparr = np.frombuffer(contents, dtype=np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # ذخیره تصویر در دیتابیس
        with get_db() as db:
            face_image = crud.create_face_image(
                db,
                person_id=person_id,
                image_data=contents  # ارسال bytes مستقیماً
            )
        
        if face_image is None:
            raise HTTPException(status_code=500, detail="Failed to save face image")
        
        return {
            "face_id": face_image["id"],
            "person_id": person_id,
            "message": "Face image uploaded successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/faces/{face_id}")
def get_face(face_id: int):
    """
    دریافت تصویر چهره با ID
    """
    with get_db() as db:
        face = crud.get_face_image_by_id(db, face_id)
    
    if face is None:
        raise HTTPException(status_code=404, detail="Face not found")
    
    return {
        "id": face["id"],
        "person_id": face["person_id"],
        "created_at": face["created_at"]
    }


@router.get("/faces/person/{person_id}")
def get_person_faces(person_id: int):
    """
    دریافت تمام تصاویر چهره یک person
    """
    with get_db() as db:
        # بررسی وجود person
        person = crud.get_person(db, person_id)
        if person is None:
            raise HTTPException(status_code=404, detail="Person not found")
        
        faces = crud.get_faces_by_person(db, person_id)
    
    return {
        "person_id": person_id,
        "faces": faces
    }
