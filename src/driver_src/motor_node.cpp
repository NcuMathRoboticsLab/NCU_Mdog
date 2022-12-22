#include "ros/ros.h"
#include "i2cpwm_board/ServoArray.h"
#include "i2cpwm_board/Servo.h"


int main(int argc, char **argv){

 ros::init(argc, argv,"motor_node");
 ros::NodeHandle n;
 ros::Publisher find_servo_center_pub = n.advertise<i2cpwm_board::ServoArray>("/servos_absolute", 1);

 while (ros::ok()){

  i2cpwm_board::ServoArray servo_array_;
  i2cpwm_board::ServoArray servo_array_absolute_;

  for (int i = 1; i <= 12; i++) {
    i2cpwm_board::Servo temp_servo;
    temp_servo.servo = i;
    temp_servo.value = 0;
    servo_array_.servos.push_back(temp_servo);
  }

  servo_array_.servos[0].value = 110;
  servo_array_.servos[1].value = 371;
  servo_array_.servos[2].value = 293;
  servo_array_.servos[3].value = 90;
  servo_array_.servos[4].value = 391;
  servo_array_.servos[5].value = 317;
  servo_array_.servos[6].value = 505;
  servo_array_.servos[7].value = 217;
  servo_array_.servos[8].value = 305;
  servo_array_.servos[9].value = 497;
  servo_array_.servos[10].value = 216;
  servo_array_.servos[11].value = 328;

  servo_array_absolute_.servos = servo_array_.servos;

  //find_servo_center_pub.publish(servo_array_absolute_);
  ros::Duration(1).sleep();

 }
 
 return 0;
}
