from enum import Enum
import pygame
import sys
from pygame.locals import QUIT

class Directions(Enum):
    InValid = 0
    Up = 1
    Down = 2
    Right = 3
    Left = 4
    UpAndRight = 5
    UpAndLeft = 6
    DownAndRight = 7
    DownAndLeft = 8

class player:
    def __init__(self,PlayerDirection,tick,speed):
        self.PlayerDirection = PlayerDirection
        self.last_tick = tick
        self.speed = speed
    
    def MovePlayer(self, PlayerDirection,speed):
        if PlayerDirection == Directions.InValid:
            return [0 * speed,0 * speed]
        if PlayerDirection == Directions.UpAndLeft:
            return [-1 * speed,-1 * speed]
        if PlayerDirection == Directions.UpAndRight:
            return [1 * speed,-1 * speed]
        if PlayerDirection == Directions.DownAndLeft:
            return [-1 * speed,1 * speed]
        if PlayerDirection == Directions.DownAndRight:
            return [1 * speed,1 * speed]
        elif PlayerDirection == Directions.Right:
            return [1 * speed,0 * speed]
        elif PlayerDirection == Directions.Left:
            return [-1 * speed,0 * speed]
        elif PlayerDirection == Directions.Up:
            return [0 * speed,-1 * speed]
        elif PlayerDirection == Directions.Down:
            return [0 * speed,1 * speed]