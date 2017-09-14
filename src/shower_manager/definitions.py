# Cart Consts
X_CART_LEN = 170
Y_CART_LEN = 240


# Board consts
MOTORS_DIS = 9550

LEFT_MOTOR_X_POS = 0 # Get from Mike's code
LEFT_MOTOR_Y_POS = 0 # Get from Mike's code
RIGHT_MOTOR_X_POS = LEFT_MOTOR_X_POS + MOTORS_DIS
RIGHT_MOTOR_Y_POS = 0 # Get from Mike's code

L_BELT_START_LEN = 0 # Get from Mike's code
R_BELT_START_LEN = 0 # Get from Mike's code

# Motor consts
STEPS_IN_FULL_CIRCLE = 200.0
BELT_PITCHES_DIS = 2.0 #in milimeters
PITCHES_IN_CIRCLE = 16.0
MM_IN_SINGLE_STEP = (PITCHES_IN_CIRCLE * BELT_PITCHES_DIS) / STEPS_IN_FULL_CIRCLE # 16*2/200=0.16
    
