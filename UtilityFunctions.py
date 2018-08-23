import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import os

#Utility function for loading an RGB image using OpenCV
def loadImage(filename):
    if filename.__class__ != ''.__class__:
        return None
    img = cv2.imread(filename)
    img = img[:,:,::-1]
    return img

#
def getPointsforCalibration():
    #
    objp = np.zeros((6 * 8, 3), np.float32)
    objp[:, :2] = np.mgrid[0:8, 0:6].T.reshape(-1, 2)

    #Lists to store object points and image points from all the images.
    objpoints = [] # 3d points in real world space.
    imgpoints = [] # 2d points in image plane.

    #Create a list of calibrated images using pictures of a chessboard
    os.chdir(os.getcwd() + '\ChessBoards')
    images = glob.glob('GO*.jpg')

    #Step through the list and search for chessboards corners
    for fname in (images):
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #Find the chessboards corners
        ret, corners = cv2.findChessboardCorners(gray, (8, 6), None)

        #If found, add object points, image points
        if ret == True:
            objpoints.append(objp)
            imgpoints.append(corners)

    #Return trained points for image calibration.
    os.chdir('..')
    return objpoints, imgpoints

#
def myDistort(imageName, param):
    # Load image
    img = loadImage(imageName)
    img_shape = (img.shape[1], img.shape[0])  # Get shape of an image where x = columns and y = rows\

    # Do camera calibration given object points and image points
    objpoints, imgpoints = getPointsforCalibration()

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_shape, None, None)
    '''
    mtx = Camera matrix
    dist = Distance Coefficients
    rvecs = Rotation Vectors
    tvecs = Translation Vectors
    '''
    return cv2.undistort(img, mtx, dist * (param), None, mtx)