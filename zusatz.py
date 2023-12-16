import sqlite3
from mqtt import MqttPublisher
import json
import time
import config

class Entry:
    def __init__(self,tstamp:float,jsonstr:str) -> None:
        self.tstamp=tstamp
        print(jsonstr)
        #self.jsonstr= json.load(jsonstr)# str has no attribute read
        self.json=json.loads(jsonstr)


class DbReader:
    def __init__(self,dbname:str) -> None:
        self.dbname=dbname
        self.commands=[]
        self.conn = sqlite3.connect(self.dbname,check_same_thread=False)
        self.conn.set_trace_callback(print)
        self.cursor = self.conn.cursor()
        self.mqtt = MqttPublisher(config.BROKER, config.PORT)
        self.robot_id=self.get_robot_id()
    
    def get_commands(self,start:str="2023-12-16 14:00:00",end:str="2023-12-16 19:00:00")->list:
        self.cursor.execute("""SELECT json.data, command.tstamp FROM command INNER JOIN json ON json.json_id = command.json_id WHERE datetime(command.tstamp, 'unixepoch') BETWEEN ? AND ? AND command.robot_id=? ORDER BY tstamp ASC;""",(start,end,self.robot_id))
        for row in self.cursor.fetchall():
            self.commands.append(Entry(row[1],row[0]))
        return self.commands
    
    def get_robot_id(self)->int:
        try:
            self.cursor.execute("SELECT robot_id FROM robot WHERE name=?;",(config.ROBO_NAME,))
            self.robot_id=self.cursor.fetchone()[0]
            self.cursor.fetchall()
            return self.robot_id
        except TypeError:
         raise sqlite3.ProgrammingError(f"Robot not found in database")
    
    def send_commands(self):
        tmp=self.commands[0]
        print(f"Start sending {len(self.commands)} commands")
        for command in self.commands:
            self.mqtt.publish(config.TOPIC_ROBO_MOVEMENT,json.dumps(command.json))
            print(f"Send command: {command.json}")
            print(f"Wait {command.tstamp-tmp.tstamp} seconds until next command")
            time.sleep(command.tstamp-tmp.tstamp)
            tmp=command
        print("Finished sending commands")
            

    def close(self):
        self.mqtt.close()
    

if __name__ == '__main__':
    dbreader = DbReader("db.db")

    dbreader.get_commands()
    dbreader.send_commands()
    
