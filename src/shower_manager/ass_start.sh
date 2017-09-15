#!/bin/sh

/bin/echo 5 > /sys/class/gpio/export 
/bin/echo 6 > /sys/class/gpio/export 
/bin/echo 12 > /sys/class/gpio/export 
/bin/echo 13 > /sys/class/gpio/export 
/bin/echo 16 > /sys/class/gpio/export 
/bin/echo 19 > /sys/class/gpio/export 
/bin/echo 26 > /sys/class/gpio/export 

/bin/sleep 1

/bin/echo "out" > /sys/class/gpio/gpio5/direction 
/bin/echo "out" > /sys/class/gpio/gpio6/direction 
/bin/echo "out" > /sys/class/gpio/gpio12/direction 
/bin/echo "out" > /sys/class/gpio/gpio13/direction 
/bin/echo "out" > /sys/class/gpio/gpio16/direction 
/bin/echo "out" > /sys/class/gpio/gpio19/direction 
/bin/echo "out" > /sys/class/gpio/gpio26/direction 

/bin/sleep 1

/usr/bin/python /home/pi/shower_board.py >> /home/pi/ass_start_log.txt

