import pygame
import time
import config
from mqtt import MqttPublisher
import json
import math

class RoboSteuerung:
    def __init__(self):
        self.mqtt = MqttPublisher(config.BROKER, config.PORT)
        pygame.init()
        self.running = True
        self.x = 1000
        self.y = 1000
        self.lpressed=False
        self.rpressed=False
        self.fpressed=False
        self.bpressed=False

    def run(self):
        screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Robo Steuerung")
        clock = pygame.time.Clock()
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        while self.running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    #escape:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_UP:
                        print("up pressed")
                        self.fpressed=True
                    elif event.key == pygame.K_DOWN:
                        self.bpressed=True
                        print("down pressed")
                    elif event.key == pygame.K_LEFT:
                        self.lpressed=True
                        print("left pressed")
                    elif event.key == pygame.K_RIGHT:
                        self.rpressed=True
                        print("right pressed")
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.fpressed=False
                        print("up released")
                    elif event.key == pygame.K_DOWN:
                        self.bpressed=False
                        print("down released")
                    elif event.key == pygame.K_LEFT:
                        self.lpressed=False
                        print("left released")
                    elif event.key == pygame.K_RIGHT:
                        self.rpressed=False
                        print("right released")
            y=0
            x=0
            if self.fpressed:
                y-=100
            if self.bpressed:
                y+=100
            if self.lpressed:
                x-=100
            if self.rpressed:
                x+=100

            if not self.fpressed and not self.bpressed and not self.lpressed and not self.rpressed: 
                x, y = pygame.mouse.get_rel() # get mouse movement since last call
            pygame.mouse.set_pos((200, 200))
            #print(x, y)
            y=-y
            self.send_mqtt(x, y)
            pygame.display.flip()  
        pygame.event.set_grab(False)
        pygame.quit()
        self.send_mqtt(0, 0,force=True)
        self.mqtt.close()
    
    def calc_to_motor(self, x, y):
        
        #print(x,y)
        if y==0:
            if x<0:
                ldir="backward"
                rdir="forward"
                x=abs(x)
            else:
                ldir="forward"
                rdir="backward"
            left=x
            right=x
        else:
            if y<0:
                ldir="backward"
                rdir="backward"
            else:
                ldir="forward"
                rdir="forward"
            left=(((50+x/2)/100))*abs(y)
            right=(((50-x/2)/100))*abs(y)
            right=round(right)
            left=round(left)
            if (left+right)!=0:
                if left>=right:
                    #print(f"left: {left} right: {right}")
                    
                    
                    right=(right/left)*abs(y)
                    left=abs(y)
                    #print(f"right/left: {(right/left)}")
                    #print(f"After left: {left} right: {right}")
                else:
                    
                    left=(left/right)*abs(y)
                    right=abs(y)
                
            right=round(right)
            left=round(left)
            if left>100:
                left=100
            elif left<0:
                left=0
            if right>100:
                right=100
            elif right<0:
                right=0

    
        return {"direction":ldir,"speed":left},{"direction":rdir,"speed":right}
    
    def send_mqtt(self, x, y,force=False):
        if x!=0:
            x=x//2
        if y!=0:
            y=y//2
        if (x!=self.x or y!=self.y) or force:
            self.x=x
            self.y=y
            data=self.calc_to_motor(x, y)
            #should be converted to json: { "motor_left": { "direction": "forward", "speed": 50 }, "motor_right": { "direction": "backward", "speed": 30 } }
            json_data=json.dumps({"motor_left":data[0],"motor_right":data[1]})
            print(json_data)
            self.mqtt.publish(config.TOPIC_ROBO_MOVEMENT, json_data)

            
if __name__ == '__main__':
    robo = RoboSteuerung()
    robo.run()