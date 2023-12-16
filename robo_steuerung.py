import pygame
import time
import confing
from mqtt import MqttPublisher

class RoboSteuerung:
    def __init__(self):
        self.mqtt = MqttPublisher(confing.BROKER, confing.PORT)
        pygame.init()
        self.running = True

    def run(self):
        screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Robo Steuerung")
        clock = pygame.time.Clock()
    
        while self.running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    #escape:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            

            pygame.display.flip()  
            
if __name__ == '__main__':
    robo = RoboSteuerung()
    robo.run()