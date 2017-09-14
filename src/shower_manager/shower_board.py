import sys
import math
from time import sleep
from definitions import * 
from subprocess import Popen, PIPE, STDOUT

class Shower_board(object):
 
    
    def __init__(self):
        
        # TODO: temp until integration with Mike
        self.cart_x_pos = 500
        self.cart_y_pos = 500
        
        print 'S ' + str(3000) + ' ' + str(2800)
        sleep (0.1)
        
        
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
        # Open pipe to motor hal
        #p = Popen(['ass_motor_control.py'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
                
        # TODO change into real read from Mikel. meanwhile only increment
        self.cart_x_pos = self.cart_x_pos+10
        self.cart_y_pos = self.cart_y_pos+10
        #print "\nNew cart position: [",self.cart_x_pos," ",self.cart_y_pos,")"
        
        return self.cart_x_pos , self.cart_y_pos


    def calc_target_steps(self, mm):
    
        """
            Method translates this length into number of steps (from the motor).  
        """
                
        return int(mm / MM_IN_SINGLE_STEP) 


    
    
    ############# MAIN RUNNING METHOD #####################      
    def run(self):
    
        """Main running function of the project"""
        
        # Infinite loop to move the cart
        while (1):
              
            # Read cart target coordinates from Camera 
            x, y = self.read_target_coordinates()
            belt_new_l_mm, belt_new_r_mm = self.calc_belts_lens_from_position(x, y)
            #print "\nRequired belt length (in mm):  LEFT: ",belt_new_l_mm,"  RIGHT: ",belt_new_r_mm
            
            # Cala stes per motor
            steps_l = self.calc_target_steps(belt_new_l_mm)
            steps_r = self.calc_target_steps(belt_new_r_mm)
            
            #print "Calculated LEFT motor steps:  LEFT: ",steps_l, "   RIGHT: ",steps_r
            
            
            # call hal to pass steps to motor  
            cmd = 'M ' + str(steps_l) + ' ' + str(steps_r)            
            #stdout_data = p.communicate(input=cmd)[0]
            print cmd
            
            # wait for 100ms
            sleep(3)



############# FILE ENTRY POINT #####################

def main(argv=None):
    if argv is None:
        argv = sys.argv
    shower = Shower_board()
    shower.run()
    
    
if __name__ == "__main__":
    sys.exit(   main())        
        
        

    
