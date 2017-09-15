import sys
import math
import socket
from time import sleep
from subprocess import Popen
from definitions import * 

import ass_motor_control

class ShowerBoard(object):
  def __init__(self):
    self.cart_x_pos = 0
    self.cart_y_pos = 0
    self.zurum_process = None

  def calc_belts_lens_from_position(self, x, y):
    """
      This method returns required LEFT and RIGHT belt lengths in order 
      to be in the passed position
      
      @returns: LEFT, RIGHT
    """
    
    x += X_MARKER_TO_MOTOR
    y += Y_MARKER_TO_MOTOR

    left = math.sqrt (
      math.pow(x - X_CART_LEN/2, 2) +
      math.pow(y - Y_CART_LEN, 2)
    )
    right = math.sqrt (
      math.pow (MOTORS_DIS - X_CART_LEN/2 - x, 2) +
      math.pow (y - Y_CART_LEN, 2)
    )
  
    return left, right

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
    server_sock.setsockopt (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
          x, y = float (cmd_tokens [1]), float (cmd_tokens [2])
          # meters to millimeters
          x *= 1000
          y *= 1000
          # y position should be adjusted as if it's the sponge
          y += Y_MARKER_TO_SPONGE
          print "Setting position to ", x, ", ", y
          l_mm, r_mm = self.calc_belts_lens_from_position(x, y)
          print "Setting belt lengths to ", l_mm, ", ", r_mm

          steps_l = self.calc_target_steps(l_mm)
          steps_r = self.calc_target_steps(r_mm)
      
          print "Calculated motor steps: ", steps_l, ", ", steps_r

          ass_motor_control.set_current_position (steps_l, steps_r)

        elif cmd_tokens [0] == 'M' and len (cmd_tokens) >= 3:
          # received cart target coordinates from camera 
          x, y = float (cmd_tokens [1]), float (cmd_tokens [2])
          # meters to millimeters
          x *= 1000
          y *= 1000
          print "Moving to ", x, ", ", y
          l_mm, r_mm = self.calc_belts_lens_from_position(x, y)
          print "Required lengths (in mm): ", l_mm, ", ", r_mm
      
          # Calc stes per motor
          steps_l = self.calc_target_steps(l_mm)
          steps_r = self.calc_target_steps(r_mm)
      
          print "Calculated motor steps: ", steps_l, ", ", steps_r

          # call hal to pass steps to motor  
          ass_motor_control.set_destination (steps_l, steps_r)

        elif cmd_tokens [0] == 'Z' and len (cmd_tokens) >= 2:
          is_on = int (cmd_tokens [1])
          ass_motor_control.set_zurum (is_on)
          if is_on and self.zurum_process is None:
            self.zurum_process = Popen ('omxplayer /home/pi/zurum.mp3', shell=True)
          else:
            if self.zurum_process is not None:
              self.zurum_process.kill ()
              self.zurum_process = None
            Popen ('killall omxplayer.bin', shell=True)


############# FILE ENTRY POINT #####################

def main():
  ass_motor_control.init ()
  shower = ShowerBoard()
  shower.run()


if __name__ == "__main__":
  sys.exit(main())    

