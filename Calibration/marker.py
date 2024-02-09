import cv2
import os
import numpy as np
import json

def process_image(image_path):
    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    marker_centers = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        center_x = x + w // 2
        center_y = y + h // 2
        #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(image, (center_x, center_y), 5, (255, 0, 0), -1)
        marker_centers.append({'x': center_x, 'y': center_y})

    cv2.imshow('Markers Detected', image)
    cv2.waitKey(0)  # Wait for a key press to continue
    cv2.destroyAllWindows()

    return marker_centers

folder_path = 'opptak/' 

image_files = [f for f in os.listdir(folder_path) if f.endswith(('.raw', '.pgm', '.ppm'))]

image_markers = {}
for file in image_files:
    centers = process_image(os.path.join(folder_path, file))
    image_markers[file] = centers

with open('markers.json', 'w') as json_file:
    json.dump(image_markers, json_file, indent=4)

print("Processing complete!")
