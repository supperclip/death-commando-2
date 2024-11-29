import pygame
import sys
from pygame.locals import QUIT
from enum import Enum
import math
import random

screen = pygame.display.set_mode((1000, 700))
screenRect = screen.get_rect()

enemy_1 = pygame.image.load("x/enemy_1.png").convert_alpha()
enemy_1 = pygame.transform.rotate(enemy_1, 90)
enemy_1 = pygame.transform.scale(enemy_1, (60, 60))

enemy_2 = pygame.image.load("x/enemy_2.png").convert_alpha()
enemy_2 = pygame.transform.rotate(enemy_2, 90)
enemy_2 = pygame.transform.scale(enemy_2, (60, 60))

enemyAnimationList = [enemy_1, enemy_2]

def Animation(current_frame,maxFrames,inputFrame,time):
    frame = inputFrame
    if (current_frame % time == 0):
        frame += 1
    if (frame > maxFrames):
        frame = 0
    return frame

def GetRotationAngle(playerCoords,coordList):
    rotX = playerCoords.x - coordList[0]
    rotY = playerCoords.y - coordList[1]
    angle_radians = math.atan2(rotY, rotX) 
    angle_degrees = math.degrees(angle_radians)
    return [rotX,rotY,angle_degrees]

def MoveEnemyX(rotX,rotY,currentX,speed):
    dist = math.hypot(rotX, rotY) or 0.000001
    dirX = rotX / dist
    currentX += dirX * speed
    return currentX

def MoveEnemyY(rotX,rotY,currentY,speed):
    dist = math.hypot(rotX, rotY) or 0.000001
    dirY = rotY / dist
    currentY += dirY * speed
    return currentY

class States(Enum):
    Moving = 1
    notMoving = 2
    Attacking = 3

class EnemyLogic:

    def __init__(self,X,Y,player,speed,tick,playerMask,enemyWindUpCooldown,enemyAttackCooldown):
        self.state = States.Moving
        self.X = X
        self.Y = Y
        self.player = player
        self.speed = speed
        self.animationFrame = 0
        self.tick = tick
        self.playerMask = playerMask
        self.mask = 0
        self.rect = 0
        self.dist = 0
        self.doingLogic = False
        self.last_tick = tick
        self.enemyWindUpCooldown = enemyWindUpCooldown
        self.enemyAttackCooldown = enemyAttackCooldown
        self.hookPointData = None

    def moveEnemy(self,player,speed,tick):
        coords = [self.X,self.Y]
        now = tick
        self.animationFrame = Animation(tick,1,self.animationFrame,25)
        enemySurface = enemyAnimationList[self.animationFrame]
        enemyRotData = GetRotationAngle(player,coords)
        if (self.state == States.Moving):
            self.X = MoveEnemyX(enemyRotData[0], enemyRotData[1],self.X, speed)
            self.Y = MoveEnemyY(enemyRotData[0], enemyRotData[1],self.Y, speed)

        if (self.state == States.notMoving):
            self.doingLogic = True
            speed = speed * 1.75
            self.X = MoveEnemyX(enemyRotData[0], enemyRotData[1],self.X, -speed)
            self.Y = MoveEnemyY(enemyRotData[0], enemyRotData[1],self.Y, -speed)

            if (now - self.last_tick) >= self.enemyWindUpCooldown:
                self.last_tick = now
                self.state = States.Attacking
                self.hookPointData = GetRotationAngle(player,coords)

        if (self.state == States.Attacking):
            speed = speed * 2.65
            self.X = MoveEnemyX(self.hookPointData[0], self.hookPointData[1],self.X, speed)
            self.Y = MoveEnemyY(self.hookPointData[0], self.hookPointData[1],self.Y, speed)

            if (now - self.last_tick) >= self.enemyAttackCooldown:
                self.last_tick = now
                self.doingLogic = False

        enemyRoated = pygame.transform.rotate(enemySurface, -enemyRotData[2])
        enemyRect = enemyRoated.get_rect(center=(self.X,self.Y))
        self.mask = pygame.mask.from_surface(enemyRoated)
        self.rect = enemyRect

        screen.blit(enemyRoated,enemyRect)

    def detectPlayerHit(self,playerMask,player):
        if self.mask.overlap(playerMask,(self.rect.x - player.centerx,self.rect.y - player.centery)):
            print("test")

    def getDistanceFromPlayer(self,player):
        rotX = self.rect.x - player.centerx 
        rotY = self.rect.y - player.centery
        self.dist = math.hypot(rotX, rotY) + 0.000001
        self.dist -= 80
        self.dist = (self.dist / 20)
        #print(self.dist)

    def getEnemyState(self,tick):
        if (self.dist <= 4 and not self.doingLogic):
            self.state = States.notMoving
            self.last_tick = tick
        if (self.dist >= 4 and not self.doingLogic):
            self.state = States.Moving