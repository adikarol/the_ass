import sys
from definitions import *

class Motor(object):
    

    def __init__(self, x_pos=0, y_pos=0, belt=50):
        
        """A new Motor instance"""
        
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.belt = belt
       


    def update_belt_len(self, increase, mm):
    
        """
            This method tells the motor hom much mm should the belt len be increased/decreased.
        """
                
        steps_to_make = mm / MM_IN_SINGLE_STEP  

        set_motor_direction(increase)
        
        # loop on steps
        while (steps_to_make):
            single_step()
            steps_to_make -= 1            
            

    # Privet methods
    
    def _set_motor_direction(self, increase):
    
        # add code here that controls the direction GPIO
        return



    def _single_step(self):
         
        # add code here that performs single step        
        return

 
            
        
            
    
