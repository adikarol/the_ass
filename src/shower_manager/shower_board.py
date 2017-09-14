import sys
import math
#from cart import Cart
from motor import Motor
from time import sleep
from definitions import * 


class Shower_board(object):
 
    
    def __init__(self,
                 x_l_motor=LEFT_MOTOR_X_POS, y_l_motor=LEFT_MOTOR_Y_POS,
                 x_r_motor=RIGHT_MOTOR_X_POS, y_r_motor=RIGHT_MOTOR_Y_POS):
        
        self.l_motor = Motor(x_l_motor,y_l_motor, L_BELT_START_LEN, True)
        self.r_motor = Motor(x_r_motor,y_r_motor, L_BELT_START_LEN, False)

        # TODO: temp until integration with Mike
        self.cart_x_pos = 100
        self.cart_y_pos = 100
        
        
        
    def calc_belts_lens_from_position(self, x, y):
        
        """
            This method returns required LEFT and RIGHT belt lengths in order 
            to be in the passed position
            
            @returns: LEFT, RIGHT
        """
        
        left = math.sqrt(  math.pow( x - X_CART_LEN/2 , 2) + math.pow( y - Y_CART_LEN , 2) )
        right = math.sqrt(  math.pow( MOTORS_DIS - X_CART_LEN/2 - x , 2) + math.pow( y - Y_CART_LEN , 2) )
    
        return left, right
        
        
        
    def read_target_coordinates(self):
     
        """
            This method reads cart target coordinates from the camera
            
            @returns: cart_new_x_pos, cart_new_y_pos
        """
    
        # TODO change into real read from Mikel. meanwhile only increment
        self.cart_x_pos = self.cart_x_pos+10
        self.cart_y_pos = self.cart_y_pos+10
        return self.cart_x_pos , self.cart_y_pos

    
    
    
    ############# MAIN RUNNING METHOD #####################      
    def run(self):
    
        """Main running function of the project"""
        
        # Infinite loop to move the cart
        while (1):
              
            # Read cart target coordinates from Camera 
            x, y = self.read_target_coordinates()
            belt_new_l, belt_new_r = self.calc_belts_lens_from_position(x, y)
            print "\nRequired belt length:  LEFT: ",belt_new_l,"  RIGHT: ",belt_new_r
            
            # Update the belt of the left and right motor
            self.l_motor.update_belt_len(belt_new_l)
            self.r_motor.update_belt_len(belt_new_r)
            
            # wait for 100ms
            sleep(0.1)



############# FILE ENTRY POINT #####################

def main(argv=None):
    if argv is None:
        argv = sys.argv
    shower = Shower_board()
    shower.run()
    
    
if __name__ == "__main__":
    sys.exit(   main())        
        
        

    
