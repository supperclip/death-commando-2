import pygame
import sys
from pygame.locals import QUIT
import math
import random

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

def rotateAroundCircleX(rect,angle,radius):
    x = rect.x + 50 + math.cos(-angle - 0.25) * radius
    return x

def rotateAroundCircleY(rect,angle,radius):
    y = rect.y + 50 - math.sin(-angle - 0.25) * radius
    return y

def Animation(current_frame,maxFrames,inputFrame,time):
    frame = inputFrame
    if (current_frame % time == 0):
        frame += 1
    if (frame > maxFrames):
        frame = 0
    return frame

class gunLogic:

    def __init__(self,M1Pressed,playerRect,bulletSpeed,Tick,fireRate,rotation,lineEnd,rads,rotX,rotY,dist,recoil,playerSprites):
        self.M1Pressed = M1Pressed
        self.playerRect = playerRect
        self.bulletSpeed = bulletSpeed
        self.last_tick = Tick
        self.fireRate = fireRate
        self.rotation = rotation
        self.lineEnd = lineEnd
        self.rads = rads
        self.rotX = rotX
        self.rotY = rotY
        self.dist = dist
        self.recoil = recoil
        self.playerSprites = playerSprites
        self.gunAnimationFrame = 0
        self.playerSurface = 0
        self.newPlayerRect = 0
    
    def blitPlayer(self,playerSprites,M1Pressed,rads,playerRect,Tick):
        if (M1Pressed):
            self.gunAnimationFrame = 0 + Animation(Tick,2,self.gunAnimationFrame,10)
            playerSprite = playerSprites[self.gunAnimationFrame + 1]
            rotated_player_image = pygame.transform.rotate(playerSprite,-rads)
            playerRoatedRect = rotated_player_image.get_rect(center=playerRect.center)
            screen.blit(rotated_player_image,playerRoatedRect)
        if not (M1Pressed):
            playerSprite = playerSprites[0]
            rotated_player_image = pygame.transform.rotate(playerSprite,-rads)
            playerRoatedRect = rotated_player_image.get_rect(center=playerRect.center)
            screen.blit(rotated_player_image,playerRoatedRect)
        self.playerSurface = rotated_player_image
        self.newPlayerRect = playerRoatedRect
    
    def playerData(self,rads,playerRect,rotX,rotY,dist,recoil):
        gunPosX = rotateAroundCircleX(playerRect,rads,30)
        gunPosY = rotateAroundCircleY(playerRect,rads,30)
        bulletRect.x = gunPosX
        bulletRect.y = gunPosY
        endX = (bulletRect.x + rotX * dist)
        endY = (bulletRect.y + rotY * dist)
        endX += (endX * random.uniform(recoil[0],recoil[1]))
        endY += (endY * random.uniform(recoil[0],recoil[1]))
        self.lineEnd = endX, endY
    
    def bulletLogic(self,M1Pressed,Tick,fireRate,rotation,bulletSpeed,playerRect):
        now = Tick
        bulletRect = playerRect
        if (M1Pressed):
            if (now - self.last_tick) >= fireRate:
                self.last_tick = now
                pygame.mixer.Sound.play(rifleShot)
                bulletXlist.append(bulletRect.x)
                bulletYlist.append(bulletRect.y)
                bulletRotList.append(rotation)
                bulletEndPosListX.append(self.lineEnd[0])
                bulletEndPosListY.append(self.lineEnd[1])

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

    def returnPlayerSurface(self):
        return self.playerSurface
    
    def returnPlayerRect(self):
        return self.newPlayerRect
