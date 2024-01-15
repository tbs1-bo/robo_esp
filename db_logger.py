import sqlite3
import config
import json
from mqtt import MqttSubscriber
import time

class DbLogger:
    def __init__(self,dbname:str,topic:str) -> None:
        self.dbname=dbname
        self.conn = sqlite3.connect(self.dbname,check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.mqtt = MqttSubscriber(config.BROKER, config.PORT)
        self.mqtt.change_callback(self.on_message)
        self.mqtt.subscribe(topic)
        self.json_data = None

    
    def on_message(self, client, userdata, msg):
        #print("message received from ",msg.topic)
        self.json_data = json.loads(msg.payload)
        json_id=self.save_raw_data()
        robot_id=self.save_robot(msg.topic.split("/")[1])
        command_id=self.save_command(robot_id,json_id)
        self.save_motor_command(command_id)
        self.conn.commit()
        print("message received from ",msg.topic)

    def save_raw_data(self)->int:
        current_jsons=[]
        self.cursor.execute("SELECT count(*) FROM json WHERE data=?;",(str(json.dumps(self.json_data)),))
        
        if self.cursor.fetchone()[0]==0:
            self.cursor.execute("INSERT INTO json (data) VALUES (?);",(json.dumps(self.json_data),))
        self.cursor.fetchall()
        self.cursor.execute("SELECT json_id FROM json WHERE data=? LIMIT 1;",(json.dumps(self.json_data),))
       
        json_id=self.cursor.fetchone()[0]
        self.cursor.fetchall()
        return json_id
    
    def save_robot(self,robot_name:str)->int:
        self.cursor.execute("SELECT count(*) FROM robot WHERE name=?;",(robot_name,))
        if self.cursor.fetchone()[0]==0:
            self.cursor.execute("INSERT INTO robot (name) VALUES (?);",(robot_name,))
        self.cursor.fetchall()
        self.cursor.execute("SELECT robot_id FROM robot WHERE name=? LIMIT 1;",(robot_name,))
        robot_id=self.cursor.fetchone()[0]
        self.cursor.fetchall()
        return robot_id

    def save_command(self,robot_id:int,json_id:int)->int:
        self.cursor.execute("INSERT INTO command (robot_id,json_id,tstamp) VALUES (?,?,?);",(robot_id,json_id,time.time()))
        self.cursor.fetchall()
        self.cursor.execute("SELECT command_id FROM command WHERE robot_id=? AND json_id=? LIMIT 1;",(robot_id,json_id))
        command_id=self.cursor.fetchone()[0]
        self.cursor.fetchall()
        return command_id
    
    def save_motor(self,motor_name:str)->int:
        self.cursor.execute("SELECT count(*) FROM motor WHERE name=?;",(motor_name,))
        if self.cursor.fetchone()[0]==0:
            self.cursor.execute("INSERT INTO motor (name) VALUES (?);",(motor_name,))
        self.cursor.fetchall()
        self.cursor.execute("SELECT motor_id FROM motor WHERE name=? LIMIT 1;",(motor_name,))
        motor_id=self.cursor.fetchone()[0]
        self.cursor.fetchall()
        return motor_id
    
    def save_direction(self,direction:str)->int:
        self.cursor.execute("SELECT count(*) FROM direction WHERE name=?;",(direction,))
        if self.cursor.fetchone()[0]==0:
            self.cursor.execute("INSERT INTO direction (name) VALUES (?);",(direction,))
        self.cursor.fetchall()
        self.cursor.execute("SELECT direction_id FROM direction WHERE name=? LIMIT 1;",(direction,))
        direction_id=self.cursor.fetchone()[0]
        self.cursor.fetchall()
        return direction_id

    def save_motor_command(self,command_id:int):
        for motor_name,motor in self.json_data.items():
            self.cursor.execute("INSERT INTO motor_command (command_id,motor_id,direction_id,speed) VALUES (?,?,?,?);",(command_id,self.save_motor(motor_name),self.save_direction(motor['direction']),motor['speed']))
        
    def close(self):
        self.mqtt.close()
        self.cursor.close()
        self.conn.commit()
        self.conn.close()

if __name__ == '__main__':
    db_logger = DbLogger("db.db","robos/+/movement")
    input("Press Enter to continue...")
    db_logger.close()

