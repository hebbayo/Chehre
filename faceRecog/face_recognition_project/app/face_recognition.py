# app/face_recognition.py
import cv2
import numpy as np
from typing import List, Tuple, Optional, Dict, Any
import pickle
import os
from pathlib import Path

class FaceRecognizer:
    def __init__(self):
        self.cascade = self._load_cascade()
        self.embeddings_file = "face_embeddings.pkl"
        self.known_embeddings: Dict[int, List[np.ndarray]] = {}
        self._load_embeddings()
    
    def _load_cascade(self) -> cv2.CascadeClassifier:
        """بارگذاری Haar Cascade برای تشخیص چهره"""
        cascade_path = "haarcascade_frontalface_default.xml"
        
        if not os.path.exists(cascade_path):
            # دانلود از GitHub اگر فایل موجود نباشد
            import urllib.request
            url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
            urllib.request.urlretrieve(url, cascade_path)
        
        cascade = cv2.CascadeClassifier(cascade_path)
        if cascade.empty():
            raise RuntimeError("Failed to load Haar Cascade")
        
        return cascade
    
    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """تشخیص چهره‌ها در تصویر"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces_array = self.cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # تبدیل numpy array به لیست tuple
        faces: List[Tuple[int, int, int, int]] = []
        for i in range(len(faces_array)):
            face = faces_array[i]
            x, y, w, h = int(face[0]), int(face[1]), int(face[2]), int(face[3])
            faces.append((x, y, w, h))
        
        return faces
    
    def _extract_lbp_features(self, image: np.ndarray) -> np.ndarray:
        """استخراج ویژگی‌های LBP"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (128, 128))
        
        # محاسبه LBP
        lbp = np.zeros_like(gray)
        for i in range(1, gray.shape[0] - 1):
            for j in range(1, gray.shape[1] - 1):
                center = gray[i, j]
                code = 0
                code |= (gray[i-1, j-1] >= center) << 7
                code |= (gray[i-1, j] >= center) << 6
                code |= (gray[i-1, j+1] >= center) << 5
                code |= (gray[i, j+1] >= center) << 4
                code |= (gray[i+1, j+1] >= center) << 3
                code |= (gray[i+1, j] >= center) << 2
                code |= (gray[i+1, j-1] >= center) << 1
                code |= (gray[i, j-1] >= center) << 0
                lbp[i, j] = code
        
        # محاسبه هیستوگرام
        hist, _ = np.histogram(lbp.ravel(), bins=256, range=(0, 256))
        hist = hist.astype(float)
        hist /= (hist.sum() + 1e-7)
        
        return hist
    
    def _extract_hog_features(self, image: np.ndarray) -> np.ndarray:
        """استخراج ویژگی‌های HOG"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (128, 128))
        
        # محاسبه گرادیان‌ها
        gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=1)
        gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=1)
        
        mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)
        
        # تقسیم به سلول‌ها و محاسبه هیستوگرام
        cell_size = 8
        bins = 9
        features = []
        
        for i in range(0, gray.shape[0], cell_size):
            for j in range(0, gray.shape[1], cell_size):
                cell_mag = mag[i:i+cell_size, j:j+cell_size]
                cell_angle = angle[i:i+cell_size, j:j+cell_size]
                
                hist, _ = np.histogram(
                    cell_angle.ravel(),
                    bins=bins,
                    range=(0, 180),
                    weights=cell_mag.ravel()
                )
                features.extend(hist)
        
        features_array = np.array(features, dtype=np.float32)
        features_array /= (np.linalg.norm(features_array) + 1e-7)
        
        return features_array
    
    def extract_embedding(self, image: np.ndarray, face_location: Tuple[int, int, int, int]) -> np.ndarray:
        """استخراج embedding از چهره"""
        x, y, w, h = face_location
        face_img = image[y:y+h, x:x+w]
        
        # ترکیب ویژگی‌های LBP و HOG
        lbp_features = self._extract_lbp_features(face_img)
        hog_features = self._extract_hog_features(face_img)
        
        embedding = np.concatenate([lbp_features, hog_features])
        return embedding
    
    def _cosine_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """محاسبه cosine similarity"""
        dot_product = np.dot(emb1, emb2)
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)
        return float(dot_product / (norm1 * norm2 + 1e-7))
    
    def train(self, person_id: int, embeddings: List[np.ndarray]) -> None:
        """آموزش مدل با embeddings یک person"""
        self.known_embeddings[person_id] = embeddings
        self._save_embeddings()
    
    def recognize(self, embedding: np.ndarray, threshold: float = 0.6) -> Optional[int]:
        """تشخیص چهره با مقایسه embedding"""
        best_match_id: Optional[int] = None
        best_similarity = threshold
        
        for person_id, known_embs in self.known_embeddings.items():
            for known_emb in known_embs:
                similarity = self._cosine_similarity(embedding, known_emb)
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match_id = person_id
        
        return best_match_id
    
    def _save_embeddings(self) -> None:
        """ذخیره embeddings در فایل"""
        with open(self.embeddings_file, 'wb') as f:
            pickle.dump(self.known_embeddings, f)
    
    def _load_embeddings(self) -> None:
        """بارگذاری embeddings از فایل"""
        if os.path.exists(self.embeddings_file):
            with open(self.embeddings_file, 'rb') as f:
                self.known_embeddings = pickle.load(f)
