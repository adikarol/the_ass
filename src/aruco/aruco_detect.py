# source: http://www.philipzucker.com/aruco-in-opencv/

import numpy as np
import cv2
import cv2.aruco as aruco
import socket

cascPath = "cascade_frontface.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

cv_major_version = int(cv2.__version__.split('.')[0])

# 80mm
MARKER_LENGTH = 0.08

DETECT_FACES_EVERY_FRAMES = 10
CALIBRATE_EVERY_FRAMES = 100

# 28cm between rotating sponge and middle of marker #9
SHOWER_MARKER9_DISTANCE = 0.28

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
    # marker 9 - notice this one moves along x, y. z is constant
    [0.0, 0.0, 0.06],
    [0.0, 0.0, 0.06],
    [0.0, 0.0, 0.06],
    [0.0, 0.0, 0.06],
    ]


def marker_center(marker):
    assert(marker > 0 and marker <= 8)
    m = marker - 1
    return (np.array(real_world_coords[4*m]) + np.array(real_world_coords[4*m + 2])) / 2.0


def get_points_for_marker(corners, ids, m):
    """Returns the object and image points for marker #<m>. 
       This function should be removed in the future, get_point_for_markers should be used instead once usage is understood."""
    imgpoints = None
    objpoints = None
    if ids is None or corners is None:
        return objpoints, imgpoints

    for i, id in enumerate(ids):
        if id == m:
            imgpoints = [corners[i][0].tolist()]
            objpoints = [real_world_coords[(m-1)*4:m*4]]
            break
    if (objpoints is not None) and (imgpoints is not None):
        imgpoints = np.array([imgpoints], dtype=np.float32)
        objpoints = np.array([objpoints], dtype=np.float32)
    return objpoints, imgpoints


def get_points_for_markers(corners, ids, markers):
    """Returns an array by marker id (from <markers>) of object-points with matching image-points."""
    imgpoints = []
    objpoints = []
    detected = []
    for m in markers:
        # find marker 'm'
        for i, id in enumerate(ids):
            if id == m:
                imgpoints.extend(corners[i][0].tolist())
                objpoints.extend(real_world_coords[(m-1)*4:m*4])
                detected.append(m)
                break

    imgpoints = np.array([imgpoints], dtype=np.float32)
    objpoints = np.array([objpoints], dtype=np.float32)
    return objpoints, imgpoints, detected

    
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
        print "found a face at %d, %d, %d, %d" % (x, y, w, h)
        cv2.rectangle(gray, (x,y), (x+w, y+h), (0, 255, 0), 2)

        # Print the coordinates of the face on the screen
#        coord = "(%s, %s)" % (x, y)
#        cv2.putText(gray, coord, (x+20, y), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,255),2)

        # Draw a small dot in the exact coordintas - test!
#        cv2.circle(gray, (x, y), 15, (0, 0, 255), 3)

    return gray


def detect_markers(gray):
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    # ids has the following format: [[id]], we want to simplify to [id]
    if ids is not None:
        ids = [id[0] for id in ids]
    return corners, ids


def calibrate_using_markers(corners, ids, gray_shape):
    assert(ids is not None)
#    print corners[0].shape
    objpoints, imgpoints, detected = get_points_for_markers(corners, ids, range(1, 9))
    assert(objpoints.shape[:-1] == imgpoints.shape[:-1])
# trying to reshape breaks calibration
#    print(objpoints.shape, imgpoints.shape)
#    objpoints = objpoints.reshape(objpoints.shape[1] / 4, 4, 3)
#    imgpoints = imgpoints.reshape(imgpoints.shape[1] / 4, 4, 2)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray_shape[::-1], None, None)
    rvecs, tvecs = rvecs[0], tvecs[0]
    return mtx, dist, rvecs, tvecs


######## COMM ########

motor_address = '10.0.0.1'
motor_port = 8888

motor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_to_motor(message):
#    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    s.sendto(message, (motor_ip, motor_port))
#    s.close()
    print 'send to motor ', message
    motor_socket.sendto(message, (motor_address, motor_port))


def send_motor_sponge_absolute(x, y):
    message = 'S %f %f' % (x, y)
    send_to_motor(message)

def send_motor_zoorum(z):
    message = 'Z %d' % (1 if z else 0)
    send_to_motor(message)

def send_motor_face_absolute(x, y):
    message = 'M %f %f' % (x, y)
    send_to_motor(message)
    
######## END COMM ########


frame_cnt = 0
faces = []
mtx = None
dist = None

zoorum_mode = (False, 0)   # frame-count
sent_sponge_position = False

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    assert(ret == True)
    #print(frame.shape) #480x640
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #print(parameters)

    # detect markers
    corners, ids = detect_markers(gray)

    chosen_marker = 0
    tvecs_m = None
    tvecs_9 = None
        
    # any markers detected?
    if ids is not None:

        # calibration
        if (mtx is None) or (dist is None) or (frame_cnt % CALIBRATE_EVERY_FRAMES) == 0: 
            mtx, dist, rvecs, tvecs = calibrate_using_markers(corners, ids, gray.shape)
        # squares around markers
        gray = aruco.drawDetectedMarkers(gray, corners)
            
        # find central marker (#9)
        objpoints_9, imgpoints_9 = get_points_for_marker(corners, ids, 9)
 #       print 'points9', imgpoints_9
        if imgpoints_9 is not None:
            rvecs_9, tvecs_9, _objPoints_9 = aruco.estimatePoseSingleMarkers(imgpoints_9, MARKER_LENGTH, mtx, dist)#, rvecs, tvecs)
            gray = aruco.drawDetectedMarkers(gray, imgpoints_9) #corners)
            for tvec, rvec in zip(tvecs_9, rvecs_9):
                gray = aruco.drawAxis(gray, mtx, dist, rvec, tvec, 0.08)

        # find a reference marker
        for m in range(1, 9):
            objpoints, imgpoints, detected = get_points_for_markers(corners, ids, [m])
            if len(detected) == 1:
                imgpoints = np.array([imgpoints]).astype(np.float32)  # reshape???
                rvecs_m, tvecs_m, _objPoints_m = aruco.estimatePoseSingleMarkers(imgpoints, MARKER_LENGTH, mtx, dist)#, rvecs, tvecs)
                gray = aruco.drawDetectedMarkers(gray, imgpoints) #corners)
                for tvec, rvec in zip(tvecs_m, rvecs_m):
                    gray = aruco.drawAxis(gray, mtx, dist, rvec, tvec, 0.08)
                if tvecs_m is not None:
                    chosen_marker = m
                    break

        # calc delta from #9 to chosen marker, send absolute to motor
        if (chosen_marker > 0) and (imgpoints_9 is not None):
            delta = tvecs_9[0][0] - tvecs_m[0][0]
            if chosen_marker > 1:
                delta += marker_center(chosen_marker) - marker_center(1)
#            print 'absolute', chosen_marker, delta
            if sent_sponge_position == False:
                send_motor_sponge_absolute(delta[0], delta[1])
                sent_sponge_position = True

    # face detection
    if (frame_cnt % DETECT_FACES_EVERY_FRAMES) == 0:
        faces = detect_faces(gray)

    if len(faces) > 0:
        draw_faces(gray, faces)
        if zoorum_mode[0] == False:
            send_motor_zoorum(True)
        zoorum_mode = (True, frame_cnt)
        # assume a single face
        face = faces[0]
        (x, y, w, h) = face
        # cheat, as if face is an aruco marker
        imgpoints_face = np.array([[[[x, y], [x+w, y], [x+w, y+h], [x, y+h]]]], dtype=np.float32)
        print imgpoints_face
        if mtx is not None:
            rvecs_face, tvecs_face, _objPoints_face = aruco.estimatePoseSingleMarkers(imgpoints_face, 0.20, mtx, dist)#, rvecs, tvecs)
            gray = aruco.drawDetectedMarkers(gray, imgpoints_face) #corners)
            for tvec, rvec in zip(tvecs_face, rvecs_face):
                gray = aruco.drawAxis(gray, mtx, dist, rvec, tvec, 0.08)
            if chosen_marker > 0:
                face_delta = tvecs_face[0][0] - tvecs_m[0][0]
                if chosen_marker > 1:
                    face_delta += marker_center(chosen_marker) - marker_center(1)

            print('Face delta', face_delta)
            cv2.putText(gray, '%.2f,%.2f' % (face_delta[0], face_delta[1]), (x+20, y), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,255), 2)
            send_motor_face_absolute(face_delta[0], face_delta[1] - 0.1)  # add 10cm up from center
    else:
        if zoorum_mode[0] and frame_cnt > zoorum_mode[1] + 60:
            zoorum_mode = (False, frame_cnt)
            send_motor_zoorum(False)

    # Display the resulting frame
    cv2.imshow('frame', gray)
    frame_cnt += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

