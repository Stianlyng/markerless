import cv2
import os
import numpy as np
import json

def process_image(image_path, window=True):
    # Read the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to isolate white markers
    _, thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)

    # Find contours of the white markers
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    keypoints_2d = []
    # Draw squares around the markers and calculate their center coordinates
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        center_x = x + w // 2
        center_y = y + h // 2
        cv2.circle(image, (center_x, center_y), 5, (255, 0, 0), -1)
        # Adding the center coordinates and a fixed accuracy of 1.0 to the keypoints list
        keypoints_2d.extend([center_x, center_y, 1.0])

    # Display the result
    if window:
        cv2.imshow('Markers Detected', image)
        cv2.waitKey(0)  # Wait for a key press to continue
        cv2.destroyAllWindows()

    return keypoints_2d

def create_openpose_json(image_path, keypoints_2d):
    # Format the data according to the OpenPose output format
    data = {
        "version": 1.3,
        "people": [
            {
                "person_id": [-1],
                "pose_keypoints_2d": keypoints_2d,
                "face_keypoints_2d": [],
                "hand_left_keypoints_2d": [],
                "hand_right_keypoints_2d": [],
                "pose_keypoints_3d": [],
                "face_keypoints_3d": [],
                "hand_left_keypoints_3d": [],
                "hand_right_keypoints_3d": []
            }
        ]
    }

    # Derive the JSON filename from the image filename
    json_filename = os.path.splitext(image_path)[0] + '.json'
    
    # Write the data to a JSON file
    with open(json_filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


drawWindow = True

# Specify the folder path
folder_path = 'h/'

# Get all image files in the folder
image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png', '.raw', '.pgm', '.ppm'))]

# Process each image, generate keypoints, and create a JSON file
for file in image_files:
    image_path = os.path.join(folder_path, file)
    keypoints_2d = process_image(image_path, drawWindow)
    create_openpose_json(image_path, keypoints_2d)

print("Processing and file creation complete!")
