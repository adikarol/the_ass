import sys
from cart import Cart
from motor import Motor

class Shower_board(object):
    
    def __init__(self, 
                 x_l_motor=0, y_l_motor=0,
                 x_r_motor=9550, y_r_motor=0,
                 x_cart=85, y_cart=85):
        
        """A new Shower Board instance"""
        
        self.l_motor = Motor(x_l_motor,y_l_motor)
        self.r_motor = Motor(x_r_motor,y_r_motor)
        self.cart = Cart(x_cart, y_cart)
        
        # Testing
        self.cart.print_cart_location()
    


############# MAIN #####################

def main(argv=None):
    if argv is None:
        argv = sys.argv
    shower = Shower_board()
    
    
if __name__ == "__main__":
    sys.exit(   main())        
        
        

    
