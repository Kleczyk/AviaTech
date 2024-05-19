import cv2
import face_recognition
import numpy as np
import sqlite3
import os
from scipy.spatial import distance
import time

# Initialize SQLite database
db_path = "face_encodings.db"


# Initialize database
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
    if not os.path.exists(image_path):
        raise ValueError(f"File does not exist: {image_path}")
    print(f"Loading image from: {image_path}")
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)
    if len(face_encodings) == 0:
        raise ValueError(f"No face found in image: {image_path}")
    return face_encodings[0]


# Path to reference image
reference_image_path = "f.jpg"  # Change to the correct path

# Extract and insert reference encoding
try:
    reference_encoding = extract_face_encodings(reference_image_path)
    insert_face_encoding(db_path, "reference", reference_encoding)
except ValueError as e:
    print(e)
    exit(1)


# Function to compare face encodings
def compare_faces(encoding1, encoding2, tolerance=0.6):
    return distance.euclidean(encoding1, encoding2) < tolerance


# Initialize camera
cap = cv2.VideoCapture(2)

# Initialize time for displaying verification message
display_message = False
display_start_time = 0

# Create a window and set it to full screen
cv2.namedWindow("Identity Verification", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Identity Verification", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Cannot read from camera")
        break

    # Convert frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces and extract encodings
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Get all encodings from the database
    stored_encodings = get_face_encodings(db_path)

    for face_encoding in face_encodings:
        # Compare with all stored encodings
        match = False
        for name, stored_encoding in stored_encodings:
            if compare_faces(face_encoding, stored_encoding):
                match = True
                text = f"Identity Verified: {name}"
                color = (0, 255, 0)
                display_message = True
                display_start_time = time.time()
                break
        if not match:
            text = "Identity Not Verified"
            color = (0, 0, 255)

        # Draw rectangle and display text
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # Display "GO" message if recently verified
    if display_message:
        elapsed_time = time.time() - display_start_time
        if elapsed_time < 3:  # Display for 3 seconds
            cv2.putText(frame, "GO", (frame.shape[1] // 2 - 50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            display_message = False

    cv2.imshow("Identity Verification", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
