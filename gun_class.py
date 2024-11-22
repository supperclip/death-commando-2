import pygame
import sys
from pygame.locals import QUIT
import math

pygame.init()

bullet1 = pygame.image.load("x/bullet1.png")
bulletRect = bullet1.get_rect()

rifleShot = pygame.mixer.Sound("sounds/rifleShot.wav")
rifleShot.set_volume(0.1)

screen = pygame.display.set_mode((1000, 700))
screenRect = screen.get_rect()

bulletList = []
bulletXlist = []
bulletYlist = []
bulletRotList = []
bulletEndPosListX = []
bulletEndPosListY = []

class gunLogic:

    def __init__(self,M1Pressed,playerRect,bulletSpeed,Tick,fireRate,rotation,lineEnd):
        self.M1Pressed = M1Pressed
        self.playerRect = playerRect
        self.bulletSpeed = bulletSpeed
        self.last_tick = Tick
        self.fireRate = fireRate
        self.rotation = rotation
        self.lineEnd = lineEnd
        

    def test(self,M1Pressed,playerRect,Tick,fireRate,rotation,lineEnd,bulletSpeed):
        now = Tick
        bulletRect = playerRect
        if (M1Pressed):
            if (now - self.last_tick) >= fireRate:
                self.last_tick = now
                pygame.mixer.Sound.play(rifleShot)
                bulletXlist.append(bulletRect.x)
                bulletYlist.append(bulletRect.y)
                bulletRotList.append(rotation)
                bulletEndPosListX.append(lineEnd[0])
                bulletEndPosListY.append(lineEnd[1])

        for x in range(len(bulletXlist)):
            dx = (bulletEndPosListX[x] - bulletXlist[x])
            dy = (bulletEndPosListY[x] - bulletYlist[x])

            distance = math.hypot(dx, dy)

            if distance != 0:
                dx /= distance
                dy /= distance

            bulletXlist[x] += dx * bulletSpeed
            bulletYlist[x] += dy * bulletSpeed
    
    def blitBullets(self):
        index = []
        
        if (len(bulletXlist) >= 1):
            for x in range(len(bulletXlist)):
                
                rotatedBullet = pygame.transform.rotate(bullet1, (-bulletRotList[x] + 90))

                bulletRect.x = bulletXlist[x]
                bulletRect.y = bulletYlist[x]

                if not (screenRect.contains(bulletRect)):
                    index.append(x)
                
                screen.blit(rotatedBullet,(bulletXlist[x],bulletYlist[x]))
            
            for index in sorted(index, reverse=True):
                del bulletXlist[index]
                del bulletYlist[index]
                del bulletRotList[index]  
                del bulletEndPosListX[index]
                del bulletEndPosListY[index]