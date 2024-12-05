import pygame
import sys
from pygame.locals import QUIT
import math
import random

pygame.init()

bullet1 = pygame.image.load("x/bullet1.png")
bullet1 = pygame.transform.rotate(bullet1,0)
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


class bulletLogic:
    def __init__(self, gunPosX, gunPosY, rotX, rotY, recoil, dist, rotation, bulletSpeed):
        self.gunPosX = gunPosX
        self.gunPosY = gunPosY
        self.rotX = rotX
        self.rotY = rotY
        self.recoil = recoil
        self.dist = dist
        self.rotation = rotation
        self.bulletSpeed = bulletSpeed
        self.bulletX = 0
        self.bulletY = 0
        self.dx = 0
        self.dy = 0
        self.rotatedBullet = None
        self.bulletRect = pygame.Rect(0, 0, 10, 10)

    def SpawnBullet(self):
        self.bulletRect.x = self.gunPosX
        self.bulletRect.y = self.gunPosY

    def GetRoation(self):
        recoilX = random.randint(-self.recoil, self.recoil)
        recoilY = random.randint(-self.recoil, self.recoil)

        rotY = self.rotY + recoilY
        rotX = self.rotX + recoilX

        endX = self.bulletRect.x + rotX * self.dist
        endY = self.bulletRect.y + rotY * self.dist

        self.dx = endX - self.bulletRect.x
        self.dy = endY - self.bulletRect.y

        distance = math.hypot(self.dx, self.dy)
        if distance != 0:
            self.dx /= distance
            self.dy /= distance

        self.dx *= self.bulletSpeed
        self.dy *= self.bulletSpeed

        self.rotatedBullet = pygame.transform.rotate(bullet1, (-self.rotation - 90))  # Apply the rotation

    def MoveBullet(self):
        self.bulletRect.x += self.dx
        self.bulletRect.y += self.dy

        screen.blit(self.rotatedBullet, self.bulletRect)

    def DeleteBullet(self):
        if (self.bulletRect.x >= 1000 or self.bulletRect.x <= 0):
            return True
        if (self.bulletRect.y >= 700 or self.bulletRect.y <= 0):
            return True
        
    def CheckEnemyHit(self,enemyRect):
        if self.bulletRect.colliderect(enemyRect):
            return True
        return False
    
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
        self.rotatedBullet = 0
    
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

    def canShoot(self,Tick,fireRate,M1Pressed):
        now = Tick
        if (M1Pressed):
            if (now - self.last_tick) >= fireRate:
                self.last_tick = now
                return True

    def returnPlayerSurface(self):
        return self.playerSurface
    
    def returnPlayerRect(self):
        return self.newPlayerRect