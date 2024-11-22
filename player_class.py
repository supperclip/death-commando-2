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
    def __init__(self,PlayerDirection,tick):
        self.PlayerDirection = PlayerDirection
        self.last_tick = tick
    
    def MovePlayer(self, PlayerDirection):
        if PlayerDirection == Directions.InValid:
            return [0,0]
        if PlayerDirection == Directions.UpAndLeft:
            return [-1,-1]
        if PlayerDirection == Directions.UpAndRight:
            return [1,-1]
        if PlayerDirection == Directions.DownAndLeft:
            return [-1,1]
        if PlayerDirection == Directions.DownAndRight:
            return [1,1]
        elif PlayerDirection == Directions.Right:
            return [1,0]
        elif PlayerDirection == Directions.Left:
            return [-1,0]
        elif PlayerDirection == Directions.Up:
            return [0,-1]
        elif PlayerDirection == Directions.Down:
            return [0,1]