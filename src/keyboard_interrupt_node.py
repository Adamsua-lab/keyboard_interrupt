#!/usr/bin/env python3

import rospy, binascii

from keyboard_interrupt.msg import Key

import sys, select, termios, tty

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return binascii.hexlify(bytes(key, 'utf-8'))

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('keyboard_interrupt')
    pub = rospy.Publisher('/keyboard_interrupt/key', Key, queue_size = 1)
    
    rospy.loginfo("Press \"CTRL + C\" to quit")
    key = Key()
    try:
        while not rospy.is_shutdown():
            key.code = int(getKey(), 16)
            key.header.stamp = rospy.Time.now()
            pub.publish(key)
            if key.code == 3:
                break
    
    except Exception as e:
        print(e)
        
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
