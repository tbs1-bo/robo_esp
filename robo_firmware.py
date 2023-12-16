import confing
from mqtt import MqttSubscriber
from gpiozero import Motor
import json


class RoboFirmware:
    def __init__(self):
        self.mqtt = MqttSubscriber(confing.BROKER, confing.PORT, confing.TOPIC_ROBO_MOVEMENT)
        self.motor_left = Motor(confing.PIN_FORWARD_MOTOR_LEFT, confing.PIN_BACKWARD_MOTOR_LEFT, confing.PIN_ENABLE_MOTOR_LEFT)
        self.motor_right = Motor(confing.PIN_FORWARD_MOTOR_RIGHT, confing.PIN_BACKWARD_MOTOR_RIGHT, confing.PIN_ENABLE_MOTOR_RIGHT)
        self.mqtt.change_callback(self.on_message)
        self.mqtt.subscribe(confing.TOPIC_ROBO_MOVEMENT)


    def on_message(self, client, userdata, msg):
        json_data = json.loads(msg.payload)
        m_left = json_data['motor_left']
        m_right = json_data['motor_right']
        if m_left['direction'] == 'forward':
            self.motor_left.forward(m_left['speed']/100)
        elif m_left['direction'] == 'backward':
            self.motor_left.backward(m_left['speed']/100)
        
        if m_right['direction'] == 'forward':
            self.motor_right.forward(m_right['speed']/100)
        elif m_right['direction'] == 'backward':
            self.motor_right.backward(m_right['speed']/100)

    def close(self):
        self.mqtt.close()
        self.motor_left.close()
    
if __name__ == '__main__':
    robo = RoboFirmware()
    input("Press Enter to continue...")
    robo.close()