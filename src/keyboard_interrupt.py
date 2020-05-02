#!/usr/bin/env python

import rospy

from geometry_msgs.msg import Twist
from std_msgs.msg import Bool

import sys, select, termios, tty

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)

    pub = rospy.Publisher('/keyboard_interrupt/key_pressed', Bool, queue_size = 1)
    rospy.init_node('keyboard_interrupt')
    key = rospy.get_param("/keyboard_interrupt/key", " ")
    
    key_pressed = Bool() 
    try:
        while not rospy.is_shutdown():
            this_key = getKey()
            if this_key == key:
                key_pressed.data = True
                pub.publish(key_pressed)
                key_pressed.data = False
            elif this_key == '\x03':
                break
    
    except Exception as e:
        print(e)
        
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
