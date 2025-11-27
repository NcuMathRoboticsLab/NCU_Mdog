#!/usr/bin/env python3
# -*-coding:utf-8 -*-
import rospy
from ncu_mdog.msg import servos_angle


if __name__ == '__main__':
    rospy.init_node('reset_motor', anonymous=True)
    rate = rospy.Rate(1)
    pub = rospy.Publisher('/servos_absolute', servos_angle, queue_size=1)
    foot_stand = [ -30.0, -45.0, 0.0]
    while not rospy.is_shutdown():
        servo_array = servos_angle()
        servo_array.angles = foot_stand * 4
        pub.publish(servo_array)
        rate.sleep()
