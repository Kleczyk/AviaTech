import cv2
import face_recognition
import numpy as np
import sqlite3
import os
from scipy.spatial import distance
import identity as idt


# Path to reference image
reference_image_path = "f.jpg"  # Change to the correct path

# Initialize SQLite database
db_path = "face_encodings.db"



# Initialize database
idt.initialize_database(db_path)

# Extract and insert reference encoding
try:
    reference_encoding = idt.extract_face_encodings(reference_image_path)
    idt.insert_face_encoding(db_path, "reference", reference_encoding)
except ValueError as e:
    print(e)
    exit(1)

# Function to compare face encodings
def compare_faces(encoding1, encoding2, tolerance=0.6):
    return distance.euclidean(encoding1, encoding2) < tolerance

# Initialize camera
cap = cv2.VideoCapture(2)

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
    stored_encodings = idt.get_face_encodings(db_path)

    for face_encoding in face_encodings:
        # Compare with all stored encodings
        match = False
        for name, stored_encoding in stored_encodings:
            if compare_faces(face_encoding, stored_encoding):
                match = True
                text = f"Identity Verified: {name}"
                color = (0, 255, 0)
                break
        if not match:
            text = "Identity Not Verified"
            color = (0, 0, 255)

        # Draw rectangle and display text
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    cv2.imshow("Identity Verification", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()