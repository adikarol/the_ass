# Cart Consts
X_CART_LEN = 160
Y_CART_LEN = 260


# Board consts
MOTORS_DIS = 955

LEFT_MOTOR_X_POS = 0 # Get from Mike's code
LEFT_MOTOR_Y_POS = 0 # Get from Mike's code
RIGHT_MOTOR_X_POS = LEFT_MOTOR_X_POS + MOTORS_DIS
RIGHT_MOTOR_Y_POS = 0 # Get from Mike's code


# Motor consts
STEPS_IN_FULL_CIRCLE = 200.0
BELT_PITCHES_DIS = 2.0 #in milimeters
PITCHES_IN_CIRCLE = 16.0
MM_IN_SINGLE_STEP = (PITCHES_IN_CIRCLE * BELT_PITCHES_DIS) / STEPS_IN_FULL_CIRCLE # 16*2/200=0.16
    
Y_MARKER_TO_SPONGE = 310

X_MARKER_TO_MOTOR = 70
Y_MARKER_TO_MOTOR = 140
