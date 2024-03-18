#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import os
import numpy as np
import toml
import json
import argparse

def process_image(image_path):

    config_dict = toml.load('Config.toml')
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Unable to load image at {image_path}. Check file path and integrity.")
        return []

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
        cv2.circle(image, (center_x, center_y), 7, (0, 0, 0), -1)
        # Adding the center coordinates and a fixed accuracy of 1.0 to the keypoints list
        keypoints_2d.extend([center_x, center_y, 1.0])

    # Display the result
    if config_dict['preprocessing']['draw_window'] is True:
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


def processMarkerImages(folder_path, cam):
    """
       Ex: cam is cam1_json
    """


    save_path = os.path.join('S00_MotionTrackingData', 'T00_JumpTrial', 'marker', f"{cam}_json")
    #print(save_path)

    valid_extensions = ('.jpg', '.jpeg', '.png', '.raw', '.pgm', '.ppm')
    
    image_files = [f for f in os.listdir(f"{folder_path}/{cam}") if f.endswith(valid_extensions)]
    print(folder_path)
    
    for file in image_files:
        image_path = os.path.join(folder_path, cam, file)
        keypoints_2d = process_image(image_path)
        json_save_path = os.path.join(save_path, os.path.basename(image_path.replace('.ppm','')) + ".json")
        print(json_save_path)
        create_openpose_json(json_save_path, keypoints_2d)
    
    print("Processing and file creation complete!")



def run(config_dict):

    folder_path = config_dict['preprocessing']['images_folder_path']

    if not folder_path:
        raise ValueError("No folder path provided. Please specify the folder path using --folder_path.")

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        print(f"The path {folder_path} does not exist or is not a directory.")

    dirs = os.listdir(folder_path)
    
    directories = [i for i in dirs if os.path.isdir(os.path.join(folder_path, i))]
    
    cam_directories = ['cam1', 'cam2', 'cam3']
    
    for cam in cam_directories:
        if cam in directories:
            print(f"'{cam}' exists in the listed directories.")
            processMarkerImages(folder_path, cam)
        else:
            print(f"'{cam}' does not exist in the listed directories.")


