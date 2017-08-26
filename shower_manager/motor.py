import sys

class Motor(object):
    
    def __init__(self, x_pos=0, y_pos=0, belt=50):
        
        """A new Motor instance"""
        
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.belt = belt
        
    
