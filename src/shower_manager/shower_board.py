import sys
import math
import socket
from time import sleep
from definitions import * 

import ass_motor_control

class ShowerBoard(object):
  def __init__(self):
    self.cart_x_pos = 0
    self.cart_y_pos = 0

  def calc_belts_lens_from_position(self, x, y):
    """
      This method returns required LEFT and RIGHT belt lengths in order 
      to be in the passed position
      
      @returns: LEFT, RIGHT
    """
    
    left = math.sqrt (
      math.pow(x - X_CART_LEN/2, 2) +
      math.pow(y - Y_CART_LEN, 2)
    )
    right = math.sqrt (
      math.pow (MOTORS_DIS - X_CART_LEN/2 - x, 2) +
      math.pow (y - Y_CART_LEN, 2)
    )
  
    return left, right

  def read_target_coordinates(self):
    """
      This method reads cart target coordinates from the camera
      
      @returns: cart_new_x_pos, cart_new_y_pos
    """
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

    # open a server socket and listen for commands
    server_sock = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.bind (("0.0.0.0", 8888))
    
    # Infinite loop to move the cart
    while (1):
      # Read a command
      cmds = server_sock.recv (1024)
      cmds = cmds.strip ().split ('\n')

      for cmd in cmds:
        cmd_tokens = cmd.split ()
        if cmd_tokens [0] == 'S' and len (cmd_tokens) >= 3:
          # received cart position from camera
          x, y = int (cmd_tokens [1]), int (cmd_tokens [2])
          print "Setting position to ", x, ", ", y
          l_mm, r_mm = self.calc_belts_lens_from_position(x, y)
          print "Setting belt lengths to ", l_mm, ", ", r_mm

          steps_l = self.calc_target_steps(l_mm)
          steps_r = self.calc_target_steps(r_mm)
      
          print "Calculated motor steps: ", steps_l, ", ", steps_r

          ass_motor_control.set_current_position (steps_l, steps_r)

        elif cmd_tokens [0] == 'M' and len (cmd_tokens) >= 3:
          # received cart target coordinates from camera 
          x, y = int (cmd_tokens [1]), int (cmd_tokens [2])
          print "Moving to ", x, ", ", y
          l_mm, r_mm = self.calc_belts_lens_from_position(x, y)
          print "Required lengths (in mm): ", l_mm, ", ", r_mm
      
          # Calc stes per motor
          steps_l = self.calc_target_steps(l_mm)
          steps_r = self.calc_target_steps(r_mm)
      
          print "Calculated motor steps: ", steps_l, ", ", steps_r

          # call hal to pass steps to motor  
          ass_motor_control.set_destination (steps_l, steps_r)



############# FILE ENTRY POINT #####################

def main():
  ass_motor_control.init ()
  shower = ShowerBoard()
  shower.run()


if __name__ == "__main__":
  sys.exit(main())    

