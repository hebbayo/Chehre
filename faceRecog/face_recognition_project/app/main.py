from fastapi import FastAPI
from app.routers import persons, faces
from face_recognition_project.app.routers import embeddings

app = FastAPI(
    title="Face Recognition API",
    description="API for face recognition and person management",
    version="1.0.0"
)

app.include_router(persons.router, prefix="/persons", tags=["Persons"])
app.include_router(faces.router, prefix="/faces", tags=["Faces"])
app.include_router(embeddings.router, prefix="/recognition", tags=["Recognition"])

@app.get("/")
def read_root():
    return {"message": "Face Recognition API is running"}
