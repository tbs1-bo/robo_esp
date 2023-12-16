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
            
            x, y = pygame.mouse.get_rel() # get mouse movement since last call
            pygame.mouse.set_pos((200, 200))
            #print(x, y)
            self.send_mqtt(x, y)
            pygame.display.flip()  
        pygame.event.set_grab(False)
        pygame.quit()
        self.send_mqtt(0, 0,force=True)
        self.mqtt.close()
    
    def calc_to_motor(self, x, y):
        pass
    
    def send_mqtt(self, x, y,force=False):
        if x!=0:
            x=x//2
        if y!=0:
            y=y//2
        if (x!=self.x or y!=self.y) or force:
            self.x=x
            self.y=y
            print(x, y)

            
if __name__ == '__main__':
    robo = RoboSteuerung()
    robo.run()