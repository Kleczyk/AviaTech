import cv2
import face_recognition
import numpy as np
import sqlite3
import os
from scipy.spatial import distance

# Initialize SQLite database
db_path = "face_encodings.db"

def initialize_database(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS face_encodings (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            encoding BLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_face_encoding(db_path, name, encoding):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        INSERT INTO face_encodings (name, encoding)
        VALUES (?, ?)
    ''', (name, encoding.tobytes()))
    conn.commit()
    conn.close()

def get_face_encodings(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT name, encoding FROM face_encodings')
    results = c.fetchall()
    conn.close()
    encodings = [(name, np.frombuffer(encoding, dtype=np.float64)) for name, encoding in results]
    return encodings

# Function to extract face encodings
def extract_face_encodings(image_path):
    # if not os.path.exists(image_path):
    #     raise ValueError(f"File does not exist: {image_path}")
    # print(f"Loading image from: {image_path}") sorry chcę użyć file handle
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)
    if len(face_encodings) == 0:
        raise ValueError(f"No face found in image: {image_path}")
    return face_encodings[0]

# Function to compare face encodings
def compare_faces(encoding1, encoding2, tolerance=0.6):
    return distance.euclidean(encoding1, encoding2) < tolerance
