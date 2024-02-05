# The name of the robot
ROBO_NAME = 'rob_trottmann'
# Settings for connecting the client to the broker
BROKER = "10.1.98.200"
PORT = 1883
# topic for controlling the robot
TOPIC_ROBO_MOVEMENT = f'robos/{ROBO_NAME}/movement'
# pin config for the motors
PIN_FORWARD_MOTOR_LEFT = 16
PIN_BACKWARD_MOTOR_LEFT = 13
PIN_ENABLE_MOTOR_LEFT = 26
PIN_FORWARD_MOTOR_RIGHT = 6
PIN_BACKWARD_MOTOR_RIGHT = 5
PIN_ENABLE_MOTOR_RIGHT = 12
SPEED=25