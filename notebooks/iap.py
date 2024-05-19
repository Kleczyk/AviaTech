import cv2
import face_recognition
import numpy as np
from scipy.spatial import distance
import os

# Path to reference image
reference_image_path = "f.jpg"  # Change to the correct path

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

# Extract reference encoding
try:
    reference_encoding = extract_face_encodings(reference_image_path)
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

    for face_encoding in face_encodings:
        # Compare with reference encoding
        match = compare_faces(face_encoding, reference_encoding)

        if match:
            text = "Identity Verified"
            color = (0, 255, 0)
        else:
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
