import pygame

pygame.init()
pygame.joystick.init()
print(pygame.joystick.get_count())

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(joystick.get_name())
x=0
y=0
speed=25
screen = pygame.display.set_mode((100, 100))
while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button==5:
                speed+=5
            elif event.button==4:
                speed-=5
            if speed<0:
                speed=0
            elif speed>100:
                speed=100
            print(f"speed: {speed}")
        
        elif event.type == pygame.JOYAXISMOTION:
            #print("Joystick axis moved.")
            ax=int(event.axis)
            val=int(event.value)
            if ax==0:
                if val>0:
                    x=1
                elif val<0:
                    x=-1
                elif val==0:
                    x=0
            elif ax==1:
                if val>0:
                    y=-1
                elif val<0:
                    y=1
                elif val==0:
                    y=0
            print(f"x: {x}, y: {y}")
        
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()