# source: http://www.philipzucker.com/aruco-in-opencv/

import numpy as np
import cv2
import cv2.aruco as aruco

cascPath = "cascade_frontface.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

cv_major_version = int(cv2.__version__.split('.')[0])

# 80mm
MARKER_LENGTH = 0.08
DETECT_FACES_EVERY_FRAMES = 10

cap = cv2.VideoCapture(0)

real_world_coords = [
    # marker 1
    [0.0, 0.0, 0.0],
    [0.08, 0.0, 0.0],
    [0.08, 0.08, 0.0],
    [0.0, 0.08, 0.0],
    # marker 2
    [0.39, 0.0, 0.0],
    [0.47, 0.0, 0.0],
    [0.47, 0.08, 0.0],
    [0.39, 0.08, 0.0],
    # marker 3
    [0.78, 0.0, 0.0],
    [0.86, 0.0, 0.0],
    [0.86, 0.08, 0.0],
    [0.78, 0.08, 0.0],
    # marker 4
    [0.0, 0.38, 0.0],
    [0.08, 0.38, 0.0],
    [0.08, 0.46, 0.0],
    [0.0, 0.46, 0.0],
    # marker 5
    [0.78, 0.38, 0.0],
    [0.86, 0.38, 0.0],
    [0.86, 0.46, 0.0],
    [0.78, 0.46, 0.0],
    # marker 6
    [0.0, 0.76, 0.0],
    [0.08, 0.76, 0.0],
    [0.08, 0.84, 0.0],
    [0.0, 0.84, 0.0],
    # marker 7
    [0.39, 0.76, 0.0],
    [0.47, 0.76, 0.0],
    [0.47, 0.84, 0.0],
    [0.39, 0.84, 0.0],
    # marker 8
    [0.78, 0.76 ,0.0],
    [0.86, 0.76, 0.0],
    [0.86, 0.84, 0.0],
    [0.78, 0.84, 0.0],
    ]
# make it an array of numpy vectors
#real_world_coords = [np.array(cs, dtype=np.float) for cs in real_world_coords]


def get_points_for_marker(corners, ids, m):
    """Returns the object and image points for marker #<m>"""
    imgpoints = None
    objpoints = None
    if ids is None or corners is None:
        return objpoints, imgpoints

    for i, id in enumerate(ids):
        if id == [m]:
            imgpoints = [corners[i][0].tolist()]
            objpoints = [real_world_coords[(m-1)*4:m*4]]
            break
    if (objpoints is not None) and (imgpoints is not None):
        imgpoints = np.array([imgpoints], dtype=np.float32)
        objpoints = np.array([objpoints], dtype=np.float32)
    return objpoints, imgpoints


def get_sorted_image_points(corners, ids, markers):
    """Returns a sorted array by marker id (from <markers>) of object-points with matching image-points.
       Only markers 1-8 are returned, marker #9 is dropped from the list."""
    imgpoints = []
    objpoints = []
    for m in markers:
        # find marker 'm'
        for i, id in enumerate(ids):
            if id == [m]:
                imgpoints.extend(corners[i][0].tolist())
                objpoints.extend(real_world_coords[(m-1)*4:m*4])
                break

    imgpoints = np.array(imgpoints, dtype=np.float32)
    objpoints = np.array(objpoints, dtype=np.float32)
    return objpoints, imgpoints

    
#def get_camera_calib(objpoints, imgpoints, gray):
#    #ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
#    pass

aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters =  aruco.DetectorParameters_create()


def detect_faces(gray):
    """Returns a list of detected faces in image <gray>"""
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE if cv_major_version < 3 else cv2.CASCADE_SCALE_IMAGE
    )
    return faces


def draw_faces(gray, faces):
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        print "found a face at %d,%d,%d,%d" % (x,y,w,h)
        cv2.rectangle(gray, (x,y), (x+w, y+h), (0, 255, 0), 2)

        # Print the coordinates of the face on the screen
        coord = "(%s,%s)" % (x,y)
        cv2.putText(gray, coord, (x+20,y), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,255),2)   

        # Draw a small dot in the exact coordintas - test!
        cv2.circle(gray, (x,y), 15, (0,0,255),3)

    return gray


def detect_markers(gray):
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    return corners, ids


def calibrate_using_markers(corners, ids, gray_shape):
#    if ids is None or corners is None:
#        return None, None, None, None
    objpoints, imgpoints = get_sorted_image_points(corners, ids, range(1, 9))
    assert(len(objpoints) == len(imgpoints))
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera([objpoints], [imgpoints], gray_shape[::-1], None, None)
    rvecs, tvecs = rvecs[0], tvecs[0]
    return mtx, dist, rvecs, tvecs


frame_cnt = 0
faces = []

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    assert(ret == True)
    #print(frame.shape) #480x640
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #print(parameters)

    # calibration
    corners, ids = detect_markers(gray)
    if ids is not None:
        mtx, dist, rvecs, tvecs = calibrate_using_markers(corners, ids, gray.shape)
    
        objpoints_1, imgpoints_1 = get_points_for_marker(corners, ids, 1)
        #print imgpoints_1
        if imgpoints_1 is not None:
            rvecs_1, tvecs_1, _objPoints_1 = aruco.estimatePoseSingleMarkers(imgpoints_1, MARKER_LENGTH, mtx, dist)#, rvecs, tvecs)
            #print(rvecs_1, tvecs_1)
            #print(_objPoints_1)

            gray = aruco.drawDetectedMarkers(gray, imgpoints_1) #corners)
            for tvec, rvec in zip(tvecs_1, rvecs_1):
                gray = aruco.drawAxis(gray, mtx, dist, rvec, tvec, 0.08)

        objpoints_9, imgpoints_9 = get_points_for_marker(corners, ids, 9)
        #print imgpoints_9
        if imgpoints_9 is not None:
            rvecs_9, tvecs_9, _objPoints_9 = aruco.estimatePoseSingleMarkers(imgpoints_9, MARKER_LENGTH, mtx, dist)#, rvecs, tvecs)
            #print(rvecs_9, tvecs_9)
            #print(_objPoints_9)

            gray = aruco.drawDetectedMarkers(gray, imgpoints_9) #corners)
            for tvec, rvec in zip(tvecs_9, rvecs_9):
                gray = aruco.drawAxis(gray, mtx, dist, rvec, tvec, 0.08)

        if (imgpoints_1 is not None) and (imgpoints_9 is not None):
            print tvecs_9[0] - tvecs_1[0]

    # face detection
    if (frame_cnt % DETECT_FACES_EVERY_FRAMES) == 0:
        faces = detect_faces(gray)

    draw_faces(gray, faces)

    #print(rejectedImgPoints)
    # Display the resulting frame
    #if (frame_cnt % 2) == 0:
    cv2.imshow('frame', gray)
    frame_cnt += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

