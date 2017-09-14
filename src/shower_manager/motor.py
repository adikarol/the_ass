import sys
from definitions import *

class Motor(object):
    

    def __init__(self, x_pos, y_pos, belt, is_left):
        
        """A new Motor instance"""
        
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.belt = belt
        self.is_left = is_left
       


    def update_belt_len(self, mm):
    
        """
            This method tells the motor the new requested belt lenght.
            Method translates this length into number of steps (from the motor).  
        """
                
        target_steps = int(mm / MM_IN_SINGLE_STEP)  
        
        if self.is_left:
            print "Calculated LEFT motor steps: ",target_steps
        else:
            print "Calculated RIGHT motor steps: ",target_steps

        # TODO: add call to Jon's code here            

        
            
    
