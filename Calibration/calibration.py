import numpy as np
import cv2 as cv
import glob

## Global checkerboard parameters ##

# This is the number of internal corners, so a 10x5 board will have size (9,4)
CHECKERBOARD_SIZE = (13, 9)  

# This is the maximum number of iterations. The algorithm will terminate after this many iterations even if the desired accuracy has not been achieved.
maximum_iterations = 30

# This is the desired accuracy or epsilon. The algorithm will terminate when this accuracy is achieved.
required_accuracy = 0.001

# Criteria for the subpixel corner refinement. 
SUBPIXEL_CRITERIA = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, maximum_iterations, required_accuracy)  

# Size of the search window for subpixel corner refinement
SUBPIXEL_WIN_SIZE = (6, 6)  

# Size of the dead zone in the middle of the search zone for subpixel corner refinement
SUBPIXEL_ZERO_ZONE = (-1, -1)  

def mean_error(objpoints, imgpoints, rvecs, tvecs, mtx, dist):
    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
        mean_error += error
    #print( "total error: {}".format(mean_error/len(objpoints)) )
    return mean_error/len(objpoints)
    
def print_calibration_results(mtx,dist,rvecs,tvecs):
    print(f'Camera matrix: \n{mtx}\n')
    print(f'Distortion coefficients: \n{dist}\n')
    print(f'Rotation vectors: \n{rvecs}\n')
    print(f'Translation vectors: \n{tvecs}\n')

def calibrate_camera(frames_path):
    objp = np.zeros((CHECKERBOARD_SIZE[0]*CHECKERBOARD_SIZE[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:CHECKERBOARD_SIZE[0], 0:CHECKERBOARD_SIZE[1]].T.reshape(-1,2)
    
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    
    img_path = f'cameras/{frames_path}/*'
    images = glob.glob(f'{img_path}.bmp')
    for frame in images:
    
        print(f"{frame} found!")
    
        img = cv.imread(frame)
        if img is None:
            print(f"Error loading image: {frame}")
            continue
    
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
        #cv.imshow('Original Image', img) 
        #cv.imshow('Grayscale Image', gray)
        #cv.waitKey(5000)
    
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, CHECKERBOARD_SIZE, None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            print("Chessboard corners found.")
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray, corners, SUBPIXEL_WIN_SIZE, SUBPIXEL_ZERO_ZONE, SUBPIXEL_CRITERIA)
            imgpoints.append(corners2)
            # Draw and display the corners
            cv.drawChessboardCorners(img, CHECKERBOARD_SIZE, corners2, ret)
            cv.imshow('img', img)
            cv.waitKey(500)
        else:
            print("Chessboard corners not found.")
            continue
    cv.destroyAllWindows()
    
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    
    print_calibration_results(mtx,dist,rvecs,tvecs)

    mean_e = mean_error(objpoints, imgpoints, rvecs, tvecs, mtx, dist)
    print(f'Mean error: {mean_e}')

    # Save the camera matrix and distortion coefficients
    np.savez(f'calibration_files/{frames_path}.npz', mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)
    
    return mtx, dist, rvecs, tvecs, mean_error

a = calibrate_camera('venstre')
b = calibrate_camera('midten')
c = calibrate_camera('hoyre')