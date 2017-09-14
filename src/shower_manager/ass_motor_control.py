import time
import thread

global x_pos
global y_pos
global x_dest
global y_dest
global z_active
global mot_ctrl

mot_ctrl = open ("/sys/class/gpio/gpio16/value", "wt")

def thread_func ():
  x_step = open ("/sys/class/gpio/gpio5/value", "wt")
  x_dir = open ("/sys/class/gpio/gpio6/value", "wt")

  y_step = open ("/sys/class/gpio/gpio13/value", "wt")
  y_dir = open ("/sys/class/gpio/gpio19/value", "wt")

  z_step = open ("/sys/class/gpio/gpio26/value", "wt")
  z_dir = open ("/sys/class/gpio/gpio12/value", "wt")

  global x_pos
  global y_pos
  global x_dest
  global y_dest
  global z_active

  z_dir.write ("0\n")
  z_dir.flush ()

  while True:
    # first pause for setting the step high
    time.sleep (0.004)

    if z_active:
      z_step.write ("1\n")
      z_step.flush ()

    if y_dest != 0 and y_dest != y_pos:
      if y_dest > y_pos:
        y_dir.write ("1\n")
        y_pos += 1
      else:
        y_dir.write ("0\n")
        y_pos -= 1
      y_dir.flush ()

      y_step.write ("1\n")
      y_step.flush ()

    if x_dest != 0 and x_dest != x_pos:
      if x_dest > x_pos:
        x_dir.write ("0\n")
        x_pos += 1
      else:
        x_dir.write ("1\n")
        x_pos -= 1
      x_dir.flush ()

      x_step.write ("1\n")
      x_step.flush ()

    # now pause for setting the step low
    time.sleep (0.004)

    z_step.write ("0\n")
    z_step.flush ()

    y_step.write ("0\n")
    y_step.flush ()

    x_step.write ("0\n")
    x_step.flush ()

def set_current_position (x, y):
  global x_pos
  global y_pos
  global x_dest
  global y_dest
  x_dest = x
  y_dest = y
  x_pos = x
  y_pos = y
  print "Setting the current location to %d,%d" % (x,y)

def set_destination (x, y):
  global x_dest
  global y_dest
  x_dest = x
  y_dest = y
  print "Setting the destination to %d,%d" % (x,y)

def set_zurum (z):
  global z_active
  z_active = z

def init ():
  global x_pos
  global y_pos
  global x_dest
  global y_dest
  global z_active
  global mot_ctrl

  x_pos = 0
  y_pos = 0
  x_dest = 0
  y_dest = 0
  z_active = 0

  mot_ctrl.write ("0\n")
  mot_ctrl.flush ()

  worker = thread.start_new_thread (thread_func, tuple([]))

def cleanup ():
  global mot_ctrl
  mot_ctrl.write ("1\n")
  mot_ctrl.flush ()


if __name__ == "__main__":
  import sys

  init ()

  while True:
    ln = sys.stdin.readline ().strip ()
    tokens = ln.split ()
    if tokens:
      if tokens[0] == 'S':
        if len(tokens) < 3: continue
        set_current_position (int (tokens [1]), int (tokens [2]))

      if tokens[0] == 'Z':
        if len(tokens) < 2: continue
        set_zurum (int (tokens [1]))

      if tokens[0] == 'M':
        if len(tokens) < 3: continue
        set_destination (int (tokens [1]), int (tokens [2]))

      if tokens[0] == 'Q':
        break

  cleanup ()

