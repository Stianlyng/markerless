import numpy as np
import cv2
import json

"""
Load the calibration parameters for a camera:

Usage:
load_calibration_data("venstre")['mtx']
def load_calibration_data(img_path):
    with np.load(f'calibration_files/{img_path}.npz') as data:
        return {
            'mtx': data['mtx'],
            'dist': data['dist'],
            'rvecs': data['rvecs'],
            'tvecs': data['tvecs']
        }

# Load the calibration parameters for each camera:
cam1 = load_calibration_data("venstre")
cam2 = load_calibration_data("midten")
cam3 = load_calibration_data("hoyre")

# Load the 2D image points for each camera:
with open('markers.json') as f:
    image_markers = json.load(f)


# Triangulate the 3D coordinates:
def triangulate_points(cam1, cam2, cam3, venstre, midten, hoyre):
    # Load the 2D image points for each camera:
    img1_points = np.array([[p['x'], p['y']] for p in image_markers[venstre + '.ppm']])
    img2_points = np.array([[p['x'], p['y']] for p in image_markers[midten + '.ppm']])
    img3_points = np.array([[p['x'], p['y']] for p in image_markers[hoyre + '.ppm']])


    print(cam1['mtx'])
    # Triangulate the 3D coordinates:
    points_3d = cv2.triangulatePoints(cam1['mtx'], cam2['mtx'], img1_points.T, img2_points.T)

    return points_3d

# Triangulate the 3D coordinates:
points_3d = triangulate_points(cam1, cam2, cam3, "venstre", "midten", "hoyre")
print(f"3D coordinates: {points_3d}")


import numpy as np
import cv2
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def load_calibration_data(img_path):
    with np.load(f'calibration_files/{img_path}.npz') as data:
        return {
            'mtx': data['mtx'],
            'dist': data['dist'],
            'rvecs': data['rvecs'],
            'tvecs': data['tvecs']
        }

# Load the calibration parameters for each camera:
cam1 = load_calibration_data("venstre")
cam2 = load_calibration_data("midten")
cam3 = load_calibration_data("hoyre")

# Load the 2D image points for each camera:
with open('markers.json') as f:
    image_markers = json.load(f)

def triangulate_points(cam1, cam2, cam3, venstre, midten, hoyre):
    # Load the 2D image points for each camera:
    img1_points = np.array([[p['x'], p['y']] for p in image_markers[venstre + '.ppm']])
    img2_points = np.array([[p['x'], p['y']] for p in image_markers[midten + '.ppm']])
    img3_points = np.array([[p['x'], p['y']] for p in image_markers[hoyre + '.ppm']])

    # Ensure rotation and translation vectors have correct shape
    R1, _ = cv2.Rodrigues(np.array(cam1['rvecs'][0]))
    R2, _ = cv2.Rodrigues(np.array(cam2['rvecs'][0]))
    R3, _ = cv2.Rodrigues(np.array(cam3['rvecs'][0]))
    t1 = np.array(cam1['tvecs'][0])
    t2 = np.array(cam2['tvecs'][0])
    t3 = np.array(cam3['tvecs'][0])

    # Construct the full projection matrices [R|t]
    P1 = np.hstack((np.dot(cam1['mtx'], R1), np.dot(cam1['mtx'], -np.dot(R1, t1))))
    P2 = np.hstack((np.dot(cam2['mtx'], R2), np.dot(cam2['mtx'], -np.dot(R2, t2))))
    P3 = np.hstack((np.dot(cam3['mtx'], R3), np.dot(cam3['mtx'], -np.dot(R3, t3))))

    # Triangulate the 3D coordinates
    points_4d = cv2.triangulatePoints(P1, P2, img1_points.T, img2_points.T)
    #points_3d = points_4d / points_4d[3]
    epsilon = 1e-8
    points_3d = points_4d / (points_4d[3] + epsilon)

    return points_3d[:3].T
# Triangulate the 3D coordinates:
points_3d = triangulate_points(cam1, cam2, cam3, "venstre", "midten", "hoyre")
# Plot the 3D coordinates
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(points_3d[:,0], points_3d[:,1], points_3d[:,2], c='r', marker='o')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Triangulated 3D Coordinates')
plt.show()

print(f"3D coordinates: {points_3d}")

"""

import numpy as np
import cv2
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def load_calibration_data(img_path):
    with np.load(f'calibration_files/{img_path}.npz') as data:
        return {
            'mtx': data['mtx'],
            'dist': data['dist'],
            'rvecs': data['rvecs'],
            'tvecs': data['tvecs']
        }

# Load the calibration parameters for each camera:
cam1 = load_calibration_data("venstre")
cam2 = load_calibration_data("midten")
cam3 = load_calibration_data("hoyre")

# Load the 2D image points for each camera:
with open('markers.json') as f:
    image_markers = json.load(f)

def normalize_points(points, K_inv):
    # Convert points to homogeneous coordinates
    points_homogeneous = np.hstack((points, np.ones((points.shape[0], 1))))
    # Normalize points
    points_normalized = np.dot(K_inv, points_homogeneous.T).T
    return points_normalized[:, :2]

def triangulate_points(cam1, cam2, cam3, venstre, midten, hoyre):
    # Load the 2D image points for each camera:
    img1_points = np.array([[p['x'], p['y']] for p in image_markers[venstre + '.ppm']])
    img2_points = np.array([[p['x'], p['y']] for p in image_markers[midten + '.ppm']])
    img3_points = np.array([[p['x'], p['y']] for p in image_markers[hoyre + '.ppm']])

    # Normalize image points
    img1_points_normalized = normalize_points(img1_points, np.linalg.inv(cam1['mtx']))
    img2_points_normalized = normalize_points(img2_points, np.linalg.inv(cam2['mtx']))
    img3_points_normalized = normalize_points(img3_points, np.linalg.inv(cam3['mtx']))

    # Ensure rotation and translation vectors have correct shape
    R1, _ = cv2.Rodrigues(np.array(cam1['rvecs'][0]))
    R2, _ = cv2.Rodrigues(np.array(cam2['rvecs'][0]))
    R3, _ = cv2.Rodrigues(np.array(cam3['rvecs'][0]))
    t1 = np.array(cam1['tvecs'][0])
    t2 = np.array(cam2['tvecs'][0])
    t3 = np.array(cam3['tvecs'][0])

    # Construct the full projection matrices [R|t]
    P1 = np.hstack((np.dot(cam1['mtx'], R1), np.dot(cam1['mtx'], -np.dot(R1, t1))))
    P2 = np.hstack((np.dot(cam2['mtx'], R2), np.dot(cam2['mtx'], -np.dot(R2, t2))))
    P3 = np.hstack((np.dot(cam3['mtx'], R3), np.dot(cam3['mtx'], -np.dot(R3, t3))))

    # Triangulate the 3D coordinates
    points_4d = cv2.triangulatePoints(P1, P2, img1_points_normalized.T, img2_points_normalized.T)
    epsilon = 1e-8
    points_3d = points_4d / (points_4d[3] + epsilon)

    return points_3d[:3].T

# Triangulate the 3D coordinates:
points_3d = triangulate_points(cam1, cam2, cam3, "venstre", "midten", "hoyre")

# Plot the 3D coordinates
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(points_3d[:,0], points_3d[:,1], points_3d[:,2], c='r', marker='o')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Triangulated 3D Coordinates')
plt.show()

print(f"3D coordinates: {points_3d}")