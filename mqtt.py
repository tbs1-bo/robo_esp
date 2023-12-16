import paho.mqtt.client as mqtt


broker_address = "169.254.61.140"
broker_port = 1883

topic = "test/topic"

class MqttSubscriber:
    def __init__(self,address:str="localhost",port:int=1883) -> None:
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(address, port)
        self.client.loop_start()
    
    def subscribe(self,topic:str):
        self.client.subscribe(topic)
    
    def on_message(self, client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        print("From Topic",message.topic)
        print("-----------------------")
    
    def change_callback(self,callback):
        if callable(callback):
            self.client.on_message = callback
        else:
            print("Callback is not callable")

    def close(self):
        self.client.loop_stop()
        self.client.disconnect()

class MqttPublisher:
    def __init__(self,address:str="localhost",port:int=1883) -> None:
        self.client = mqtt.Client()
        self.client.connect(address, port)
        self.client.loop_start()
    def publish(self,topic:str,message:str):
        self.client.publish(topic,message)
    def close(self):
        self.client.loop_stop()
        self.client.disconnect()
        