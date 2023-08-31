#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64

def nodo_manipulador():
    
    rospy.init_node('nodo_move_base')
    
    publisher_1 = rospy.Publisher('/joint_1_controller/command',Float64,queue_size=1)
    publisher_2 = rospy.Publisher('/joint_2_controller/command',Float64,queue_size=1)
    
    msg_1 = Float64()
    msg_2 = Float64()
    
    msg_1.data = 0.0
    msg_2.data = 1.0
    
    rate = rospy.Rate(10)  #crea un objeto rate a 10hz
    
    while not rospy.is_shutdown():
        
        #publisher_1.publish(msg_1)
        rospy.sleep(1)
        publisher_2.publish(msg_2)

if __name__ == '__main__':
    try:
        nodo_manipulador()
    except rospy.ROSInterruptException:
        pass  