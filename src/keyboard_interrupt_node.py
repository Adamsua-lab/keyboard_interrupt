#!/usr/bin/env python

import rospy, binascii

from keyboard_interrupt.msg import Key

import sys, select, termios, tty

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key.encode('hex')

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('keyboard_interrupt')
    pub = rospy.Publisher('/keyboard_interrupt/key', Key, queue_size = 1)
    
    rospy.loginfo("Press \"Esc\" key to close this node")
    key = Key()
    try:
        while not rospy.is_shutdown():
            key.code = int(getKey(), 16)
            key.header.stamp = rospy.Time.now()
            pub.publish(key)
            if key.code == Key.KEY_ESCAPE:
                break
    
    except Exception as e:
        print(e)
        
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
