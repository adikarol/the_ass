import sys

class Cart(object):

    def __init__ (self, x_pos=0, y_pos=0):
        """A new cart instance, with corresponding sizes and position.
           Cart's (x_pos, y_pos) is the position of the sponge.
        """
        
        # Consts
        X_CART_LEN = 170
        Y_CART_LEN = 240
    
        self.x_len = X_CART_LEN
        self.y_len = Y_CART_LEN
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.state = 0  #OFF by default
    
    
    
    def set_target_location (self, x_tar, y_tar):
        """ Sets the target location for the cart. 
            Cart will start moving immediately.
        """
        print "Initial Cart position:(",self.x_pos,",",self.y_pos,")"
               
    
    
    def print_cart_location (self):
           
        print "Cart position: (",self.x_pos,",",self.y_pos,")"
 
