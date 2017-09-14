# source: http://www.philipzucker.com/aruco-in-opencv/

import numpy as np
import cv2
import cv2.aruco as aruco

# 80mm
MARKER_LENGTH = 0.08

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


def get_sorted_image_points(corners, ids):
    """Returns a sorted array by marker id of object-points with matching image-points"""
    imgpoints = []
    objpoints = []
    for m in range(1, 9):
        # find marker 'm'
        for i, id in enumerate(ids):
            if id == [m]:
                imgpoints.extend(corners[i][0].tolist())
                objpoints.extend(real_world_coords[(m-1)*4:m*4])
                break

    imgpoints = np.array(imgpoints, dtype=np.float32)
    objpoints = np.array(objpoints, dtype=np.float32)
    return objpoints, imgpoints

    
def get_camera_calib(objpoints, imgpoints, gray):
    #ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    pass


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    assert(ret == True)
    #print(frame.shape) #480x640
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters =  aruco.DetectorParameters_create()

    #print(parameters)

    '''    detectMarkers(...)
        detectMarkers(image, dictionary[, corners[, ids[, parameters[, rejectedI
        mgPoints]]]]) -> corners, ids, rejectedImgPoints
        '''
        #lists of ids and the corners beloning to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
#    if len(corners) > 0:
#        print(corners[0], ids[0])
    if ids is not None and corners is not None:
        objpoints, imgpoints = get_sorted_image_points(corners, ids)
        assert(len(objpoints) == len(imgpoints))
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera([objpoints], [imgpoints], gray.shape[::-1], None, None)
        rvecs, tvecs = rvecs[0], tvecs[0]
#        print(ret, mtx)
#        print(rvecs, tvecs)
        rvecs, tvecs, _objPoints = aruco.estimatePoseSingleMarkers(corners, MARKER_LENGTH, mtx, dist, rvecs, tvecs)
        print(rvecs, tvecs)

        
    #It's working.
    # my problem was that the cellphone put black all around it. The alrogithm
    # depends very much upon finding rectangular black blobs

    gray = aruco.drawDetectedMarkers(gray, corners)
    for tvec, rvec in zip(tvecs, rvecs):
        gray = aruco.drawAxis(gray, mtx, dist, rvec, tvec, 0.08)

    #print(rejectedImgPoints)
    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

