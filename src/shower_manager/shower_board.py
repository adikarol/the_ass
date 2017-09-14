import sys
import math
from cart import Cart
from motor import Motor
from definitions import * 


class Shower_board(object):
 
    def _calc_belts_lens_from_position(self, x, y):
        
        """
            This method returns required LEFT and RIGHT belt lengths in order 
            to be in the passed position
            
            returns: LEFT, RIGHT
        """
        
        left = math.sqrt(  math.pow( x - X_CART_LEN/2 , 2) + math.pow( y - Y_CART_LEN , 2) )
        right = math.sqrt(  math.pow( MOTORS_DIS - X_CART_LEN/2 - x , 2) + math.pow( y - Y_CART_LEN , 2) )
    
        return left, right
        
        
    
    def __init__(self,
                 x_l_motor=0, y_l_motor=0,
                 x_r_motor=MOTORS_DIS, y_r_motor=0,
                 x_cart=X_CART_LEN/2, y_cart=X_CART_LEN/2):
        
        """A new Shower Board instance"""
        
        self.l_motor = Motor(x_l_motor,y_l_motor)
        self.r_motor = Motor(x_r_motor,y_r_motor)
        self.cart = Cart(x_cart, y_cart)
        
        # Testing only
        self.cart.print_cart_position()
        
        print self._calc_belts_lens_from_position(x_cart, y_cart)



############# MAIN #####################

def main(argv=None):
    if argv is None:
        argv = sys.argv
    shower = Shower_board()
    
    
if __name__ == "__main__":
    sys.exit(   main())        
        
        

    
