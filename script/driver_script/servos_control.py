#!/usr/bin/env python3
# -*-coding:utf-8 -*-
import numpy as np

import rospy
from ncu_mdog.msg import servos_angle, Servo, ServoArray
from uart_servo_controller import UART_Servo_Controller

uart_crtl = None

servos_center = np.zeros(12, dtype=float)
default_certer = [500.0] * 12

servos_range = np.zeros(12, dtype=float)
default_range = [750.0] * 12

servos_direction = np.zeros(12, dtype=float)
default_direction = [ 1, 1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1]
                              
_servos_angle = servos_range/180.0


def unload_all_servos() -> None:
    rospy.loginfo('Shutting down... unloading all servos.')
    uart_crtl.cmd_mult_servo_unload(list(range(1,13)))


def servos_angle_callback(data):
    servo_array = ServoArray()
    temp_array = []
    servo_to_move = list(range(1, 13))
    for i in range(12):
        temp_servo = Servo()
        temp_servo.servo = i+1
        temp_servo.value = 0
        servo_array.servos.append(temp_servo)
        if data.angles[i] == 1.0: # use 1.0 for no movement
            servo_to_move.remove(i + 1)
            servo_array.servos[i].value = 1.0
        else:
            temp = int(round((data.angles[i] * _servos_angle[i] * servos_direction[i]) + servos_center[i]))
            servo_array.servos[i].value = temp
            temp_array.append(temp)

    pub.publish(servo_array)
    uart_crtl.cmd_servo_move(servo_to_move, temp_array, 100)

    voltage = uart_crtl.cmd_get_battery_voltage()
    if voltage >= 5.0: pass
    elif 4.1 <= voltage < 5.0:
        rospy.logwarn(f'Now voltage of servos: {voltage}')
    else:
        rospy.logdebug(f'Now voltage of servos: {voltage}')
        rospy.logerr('Now voltage of servos is lower than 4.1, shutting down...')
        rospy.signal_shutdown('SERVOS VOLTAGE LOW')


if __name__ == '__main__':
    rospy.init_node('servos_control', anonymous=True)
    rospy.on_shutdown(unload_all_servos)
    pub = rospy.Publisher('/servos_absolute', ServoArray, queue_size = 1)  # for debug

    com_port = rospy.get_param('~com_port', '/dev/ttyTHS1')
    center = rospy.get_param('~center', default_certer)
    range = rospy.get_param('~range', default_range)
    direction = rospy.get_param('~direction', default_direction)

    uart_crtl = UART_Servo_Controller(com_port)
    servos_center = np.array(center)
    servos_range = np.array(range)
    servos_direction = np.array(direction)
    _servos_angle = servos_range/180.0

    rospy.Subscriber('/servos_angle', servos_angle, servos_angle_callback)
    rospy.spin()
