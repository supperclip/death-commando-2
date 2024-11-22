import pygame
import sys
from pygame.locals import QUIT
import random
import math
from player_class import player
from player_class import Directions
from gun_class import gunLogic

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("death commando: pest control II")
clock = pygame.time.Clock()

background = pygame.image.load("x/background.png")

current_frame = 0
Tangle_degrees = 0


#player data
Current_Direction = Directions.InValid
MoveSpeed = 0.8
Tangle_radians = 0

M_pressed = False

player_1 = pygame.image.load("x/player_1.png")
player_1 = pygame.transform.rotate(player_1, 90)
playerRect = player_1.get_rect()

playerShoot1 = pygame.image.load("x/player_shoot_1.png").convert_alpha()
playerShoot1 = pygame.transform.rotate(playerShoot1, 90)

p = player(Current_Direction,current_frame)

#gun data:
bulletSpeed = 15
fireRate = 6
angle_offset = 3
circleRotation = 0

gunSurface = pygame.Surface((10,10))
gunRect = gunSurface.get_rect()
gunRect.x = playerRect.x
gunRect.y = playerRect.y

lineEnd = 0

crosshair = pygame.image.load("x/crosshair.png")
crosshair = pygame.transform.scale(crosshair, (35, 35))
cursor = pygame.cursors.Cursor((17,17), crosshair)
pygame.mouse.set_cursor(cursor)


BLACK = (0,0,0)
WHITE = (255,255,255)

bullet1 = pygame.image.load("x/bullet1.png")

guns = gunLogic(M_pressed,gunRect,bulletSpeed,current_frame,fireRate,Tangle_degrees,lineEnd)

def rotateLines(origin, point, angle):
    ox, oy = origin
    px, py = point
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    qx = ox + cos_angle * (px - ox) - sin_angle * (py - oy)
    qy = oy + sin_angle * (px - ox) + cos_angle * (py - oy)
    return (qx, qy)

def rotateAroundCircleX(rect,angle,radius):
    x = rect.x + 50 + math.cos(-angle - 0.25) * radius
    return x

def rotateAroundCircleY(rect,angle,radius):
    y = rect.y + 50 - math.sin(-angle - 0.25) * radius
    return y

while True:

    current_frame += 1
    
    screen.blit(background, (0, 0))  
    
    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and keys[pygame.K_w]:
        Current_Direction = Directions.UpAndLeft
    elif keys[pygame.K_d] and keys[pygame.K_w]:
         Current_Direction = Directions.UpAndRight
    elif keys[pygame.K_d] and keys[pygame.K_s]:
        Current_Direction = Directions.DownAndRight
    elif keys[pygame.K_a] and keys[pygame.K_s]:
        Current_Direction = Directions.DownAndLeft
    elif keys[pygame.K_a]:
        Current_Direction = Directions.Left
    elif keys[pygame.K_w]:
        Current_Direction = Directions.Up
    elif keys[pygame.K_d]:
        Current_Direction = Directions.Right
    elif keys[pygame.K_s]:
        Current_Direction = Directions.Down
    else:
        Current_Direction = Directions.InValid

    mouse_buttons = pygame.mouse.get_pressed()
    M_pressed = mouse_buttons[0]
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    playerList = p.MovePlayer(Current_Direction)
    playerMoveX = (playerList[0] * MoveSpeed)
    playerMoveY = (playerList[1] * MoveSpeed)
    playerRect.x += playerMoveX
    playerRect.y += playerMoveY
    TrotX = mouse_x - playerRect.centerx 
    TrotY = mouse_y - playerRect.centery
    Tdist = math.hypot(TrotX, TrotY) + 0.000001  # prevents division by zero
    TdirX = (TrotX / Tdist) + 0.00000000001
    TdirY = (TrotY / Tdist) + 0.00000000001
    Tangle_radians = math.atan2(TrotY, TrotX)
    Tangle_degrees = math.degrees(Tangle_radians)

    rotated_player_image = pygame.transform.rotate(player_1,-Tangle_degrees)
    playerRoatedRect = rotated_player_image.get_rect(center=playerRect.center)
    playerMask = pygame.mask.from_surface(rotated_player_image)

    gunPosX = rotateAroundCircleX(playerRect,Tangle_radians,30)
    gunPosY = rotateAroundCircleY(playerRect,Tangle_radians,30)

    gunRect.x = gunPosX
    gunRect.y = gunPosY

    gunLineX = rotateAroundCircleX(playerRect,Tangle_radians,35)
    gunLineY = rotateAroundCircleY(playerRect,Tangle_radians,35)
    
    endX = (playerRect.x + TrotX * Tdist)
    endY = (playerRect.y + TrotY * Tdist)
    lineStart = (((gunLineX),(gunLineY)))
    lineEnd = endX, endY

    line1_end = rotateLines(lineEnd, lineStart, angle_offset)
    line2_end = rotateLines(lineEnd, lineStart, -angle_offset)

    #pygame.draw.line(screen, BLACK, lineStart, lineEnd, 2)
    pygame.draw.line(screen, BLACK, lineStart, line1_end, 2)
    pygame.draw.line(screen, BLACK, lineStart, line2_end, 2)
    
    #screen.blit(gunSurface,(gunPosX,gunPosY)) 
    #pygame.draw.rect(screen, (255, 0, 0),gunRect , 2)

    screen.blit(rotated_player_image, playerRoatedRect.topleft)
    
    guns.test(M_pressed,gunRect,current_frame,fireRate,Tangle_degrees,lineEnd,bulletSpeed)
    guns.blitBullets()

    pygame.display.update()
    clock.tick(60)