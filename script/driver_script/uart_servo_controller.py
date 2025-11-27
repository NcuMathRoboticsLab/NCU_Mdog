#!/usr/bin/env python3
# -*-coding:utf-8 -*-
import serial
import time


class UART_Servo_Controller:
    """
    Functions:
        cmd_servo_move
        cmd_mult_servo_pos_read
        cmd_mult_servo_unload
        cmd_get_battery_voltage
        cmd_servo_temperature_read
    """
    def __init__(self, com_port, baudrate=9600):
        """
        param:
            dev: string
            baud_rate: int
        """
        self.ser = serial.Serial()
        self.ser.baudrate = baudrate
        self.ser.port = com_port
        self.ser.open()
        self.ser.flush()
        time.sleep(1.0)


    def __del__(self):
        self.ser.close()


    def cmd_servo_move(self, servo_id, angle_position, time):
        """
        Control single/multi servos
        param: 
            servo_id: list
                e.g. servo_id = [1, 2, 3, 4]   
            angle_position: list[int(0~1000)]
                e.g. angle_position = [500, 600, 700, 800]  
            time: int (ms)
                e.g. time = 1000    
        """
        data = bytearray(b'\x55\x55')                # header 
        data.extend([0xff & (len(servo_id)*3+5)])    # length (the number of control servo * 3 + 5)
        data.extend([0x03])                          # command value

        data.extend([0xff & len(servo_id)])          # The number of servo to be controlled
        
        time = 0xffff & time
        data.extend([(0xff & time), (0xff & (time >> 8))])   # Lower and Higher 8 bits of time value

        for i in range(len(servo_id)):
            p_val = 0xffff & angle_position[i]
            data.extend([0xff & servo_id[i]])    # servo id
            data.extend([(0xff & p_val), (0xff & (p_val >> 8))])   # Lower and Higher 8 bits of angle posiotion value
             
        self.ser.write(data) 


    def cmd_mult_servo_unload(self, servo_id):
        """
        Relax the specific servos
        param: 
            servo_id: list
                e.g. servo_id = [1, 2, 3, 4]     
        """
        data = bytearray(b'\x55\x55')                # header 
        data.extend([0xff & (len(servo_id)+3)])      # length (the number of control servo + 3)
        data.extend([0x14])                          # command value

        data.extend([0xff & len(servo_id)])          # The number of servo to be controlled.

        for i in range(len(servo_id)):
            data.extend([0xff & servo_id[i]])    # servo id

        self.ser.write(data)


    def cmd_mult_servo_pos_read(self, servo_id):
        """
        Read the value (0~1000) of specific servos
        param: 
            servo_id: list
                e.g. servo_id = [1, 2, 3, 4]   
        return: 
            angle_pos_values: list[int(0~1000)]
        """
        # transmit
        data = bytearray(b'\x55\x55')            # header 
        data.extend([0xff & (len(servo_id)+3)])  # length (the number of control servo + 3)
        data.extend([0x15])                      # command value
        data.extend([0xff & len(servo_id)])      # The number of servo to be controlled.

        for i in range(len(servo_id)):
            data.extend([0xff & servo_id[i]])    # servo id

        # Empty the contents of the cache in preparation for receiving data.
        count = self.ser.inWaiting()    # Check receive cache.
        if count != 0:
            _ = self.ser.read(count)    # Read out data
        # Send command.
        self.ser.write(data)

        # Receive
        count = 0
        recv_cmd_len = len(servo_id) * 3 + 5
        angle_pos_values = servo_id[:]  # Create a list whose size is the same as the number of servos you want to get values from.
        while count != recv_cmd_len:        # Waiting for reception to finish.
            count = self.ser.inWaiting()
        recv_data = self.ser.read(count)    # Read the received byte data.
        #print(recv_data)
        #print(type(recv_data))
        #print(recv_data[2:])
        #print()
        #print(str(recv_data))
        #print(type(str(recv_data)))
        if count == recv_cmd_len:           # Check if the number of bytes of data received is correct as a response to this command.
            if recv_data[0] == 0x55 and recv_data[1] == 0x55 and recv_data[3] == 0x15:  # Check if the received data is a response to a command.
                #print('Yes')
                for i in range(len(servo_id)):
                    angle_pos_values[i] = 0xffff & (recv_data[6+3*i] | (0xff00 & (recv_data[7+3*i] << 8)))
        
        return angle_pos_values


    def cmd_get_battery_voltage(self):
        """
        Read the voltage of servos
        return: 
            battery_voltage: float (V)
        """
        # transmit
        data = bytearray(b'\x55\x55')    # header 
        data.extend([0x02])              # length
        data.extend([0x0F])              # command value
        # Empty the contents of the cache in preparation for receiving data.
        self.ser.reset_input_buffer()
        count = self.ser.inWaiting()    # Check receive cache.
        if count != 0:
            _ = self.ser.read(count)    # Read out data
        # Send command.
        self.ser.write(data)

        # Receive
        count = 0
        recv_cmd_len = 6
        while count != recv_cmd_len:        # Waiting for reception to finish.
            count = self.ser.inWaiting()
        recv_data = self.ser.read(count)    # Read the received byte data.
        if count == recv_cmd_len:                      # Check if the number of bytes of data received is correct as a response to this command.
            if recv_data[0] == 0x55 and recv_data[1] == 0x55 and recv_data[3] == 0x0F : # Check if the received data is a response to a command.
                battery_voltage = 0xffff & (recv_data[4] | (0xff00 & (recv_data[5] << 8))) # Read battery  voltage
                battery_voltage = battery_voltage / 1000.0

        return battery_voltage
