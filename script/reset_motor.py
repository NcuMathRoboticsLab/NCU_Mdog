#!/usr/bin/python

import rospy
from i2cpwm_board.msg import ServoArray
from i2cpwm_board.msg import Servo
if __name__ == "__main__":
    rospy.init_node('reset_motor', anonymous=True)
    rate = rospy.Rate(1)
    pub = rospy.Publisher('/servos_absolute', ServoArray,queue_size=1)
    servo_array_ = ServoArray()
    servo_array_absolute_ = ServoArray();
    while not rospy.is_shutdown():
        for i in range(1,13):
            temp_servo = Servo()
            temp_servo.servo = i
            temp_servo.value = 0
            servo_array_.servos.append(temp_servo)
    	servo_array_absolute_.servos = servo_array_.servos
        pub.publish(servo_array_absolute_)
        rate.sleep()
