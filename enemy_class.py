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

    def __init__(self,state,X,Y,player,speed,tick,playerMask):
        self.state = state
        self.X = X
        self.Y = Y
        self.Player = player
        self.speed = speed
        self.animationFrame = 0
        self.tick = tick
        self.playerMask = playerMask
        self.mask = 0
        self.rect = 0

    def moveEnemy(self,state,player,speed,tick):
        coords = [self.X,self.Y]

        self.animationFrame = Animation(tick,1,self.animationFrame,25)
        enemySurface = enemyAnimationList[self.animationFrame]
        if (state == States.Moving):
            enemyRotData = GetRotationAngle(player,coords)
            self.X = MoveEnemyX(enemyRotData[0], enemyRotData[1],self.X, speed)
            self.Y = MoveEnemyY(enemyRotData[0], enemyRotData[1],self.Y, speed)
            enemyRoated = pygame.transform.rotate(enemySurface, -enemyRotData[2])
            enemyRect = enemyRoated.get_rect(center=(self.X,self.Y))
            self.mask = pygame.mask.from_surface(enemyRoated)
            self.rect = enemyRect
        screen.blit(enemyRoated,enemyRect)

    def detectPlayerHit(self,playerMask,player):
        if playerMask.overlap(self.mask,(self.rect.x - player.centerx,self.rect.y - player.centery)):
            print("test")