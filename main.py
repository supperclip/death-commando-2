import pygame
import sys
from pygame.locals import QUIT
import random
import math
from player_class import player
from player_class import Directions
from gun_class import gunLogic
from gun_class import bulletLogic
from enemy_class import EnemyLogic
from enemy_class import States
from enemy_class import Gargoyle
from enemy_class import Brute
from gameLogic_class import gameLogic

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("death commando: pest control II")
clock = pygame.time.Clock()

background = pygame.image.load("x/background.png")

current_frame = 0
Tangle_degrees = 0

testSurface = pygame.Surface((20,20))
testSurface.fill("black")

playerPathFindRect = pygame.surface.Surface((45,45))
playerPathFindRect = playerPathFindRect.get_rect()

player_1 = pygame.image.load("x/player_1.png")
player_1 = pygame.transform.rotate(player_1, 90)
playerRect = player_1.get_rect()

playerShoot1 = pygame.image.load("x/player_shoot_1.png").convert_alpha()
playerShoot1 = pygame.transform.rotate(playerShoot1, 90)

playerShoot2 = pygame.image.load("x/player_shoot_2.png").convert_alpha()
playerShoot2 = pygame.transform.rotate(playerShoot2, 90)

playerShoot3 = pygame.image.load("x/player_shoot_3.png").convert_alpha()
playerShoot3 = pygame.transform.rotate(playerShoot3, 90)

playerFlex1 = pygame.image.load("x/player_FLEX_1.png")
playerFlex1 = pygame.transform.rotate(playerFlex1, 90)

playerFlexShoot1 = pygame.image.load("x/player_FLEX_shoot1.png")
playerFlexShoot1 = pygame.transform.rotate(playerFlexShoot1, 90)

playerFlexShoot2 = pygame.image.load("x/player_FLEX_shoot2.png")
playerFlexShoot2 = pygame.transform.rotate(playerFlexShoot2, 90)

playerFlexShoot3 = pygame.image.load("x/player_FLEX_shoot3.png")
playerFlexShoot3 = pygame.transform.rotate(playerFlexShoot3, 90)

bullet1 = pygame.image.load("x/bullet1.png")
bulletMask = pygame.mask.from_surface(bullet1)

FLEXList = [playerFlex1,playerFlexShoot1,playerFlexShoot2,playerFlexShoot3]
ravagerMK1List = [player_1,playerShoot1,playerShoot2,playerShoot3]

ravagerShell = pygame.image.load("x/ravagerShell.png")

bullet1 = pygame.image.load("x/bullet1.png")

playerSprites = ravagerMK1List

#sounds
bulletHit = pygame.mixer.Sound("sounds/bulletImpact.wav")
bulletHit.set_volume(0.25)

ravagerShot = pygame.mixer.Sound("sounds/rifleShot.wav")
ravagerShot.set_volume(4)

#player data
Current_Direction = Directions.InValid
MoveSpeed = 1.2
Tangle_radians = 0

M_pressed = False

playerMask = pygame.mask.from_surface(player_1)

#gun data:
bulletList = []

bulletSpeed = 7.5
fireRate = 15
bulletDamage = 15

bulletX = 0
bulletY = 0

currentGun = "FLEX raider MK1"

TrotX = 0
TrotY = 0
Tdist = 0
Tangle_degrees = 0

gunSurface = pygame.Surface((10,10))
gunRect = gunSurface.get_rect()
gunRect.x = playerRect.x
gunRect.y = playerRect.y

recoil = 45

lineEnd = 0

crosshair = pygame.image.load("x/crosshair.png")
crosshair = pygame.transform.scale(crosshair, (35, 35))
cursor = pygame.cursors.Cursor((17,17), crosshair)
pygame.mouse.set_cursor(cursor)

#Gargoyle data:
gargoyleX = random.randint(0,1000)
gargoyleY = 0
gargoyleSpeed = 1.6
gargoyleHealth = 15
gargoyleList = []
gargoyleDeath = pygame.mixer.Sound("sounds/enemy3.wav")
gargoyleDeath.set_volume(2.5)

#brute data
bruteX = random.randint(0,1000)
bruteY = 0
bruteSpeed = 1.15
bruteHealth = 125
bruteWindUpCooldown = 20
bruteAttackCooldown = 60
bruteList = []

BLACK = (0,0,0)
WHITE = (255,255,255)

bullet1 = pygame.image.load("x/bullet1.png")

guns = gunLogic(M_pressed,gunRect,bulletSpeed,current_frame,fireRate,Tangle_degrees,lineEnd,Tangle_radians,TrotX,TrotY,Tdist,recoil,playerSprites)
p = player(Current_Direction,current_frame,MoveSpeed)
logic = gameLogic()


def rotateAroundCircleX(rect,angle,radius):
    x = rect.x + 50 + math.cos(-angle - 0.25) * radius
    return x

def rotateAroundCircleY(rect,angle,radius):
    y = rect.y + 50 - math.sin(-angle - 0.25) * radius
    return y

def GunFunction(gun):
    if (gun == "FLEX raider MK1"):
        bulletSpeed = 17
        fireRate = 6
        animationList = FLEXList
    
def Delay(inputFrame,frame,delay):
    if (inputFrame == (frame + delay)):
        return True
    else:
        return False

while True:
    
    current_frame += 1
    
    screen.blit(background, (0, 0))  
    
    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    mouse_buttons = pygame.mouse.get_pressed()
    M_pressed = mouse_buttons[0]

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

    mouse_x, mouse_y = pygame.mouse.get_pos()
    playerList = p.MovePlayer(Current_Direction,MoveSpeed)
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

    playerPathFindRect.center = playerRect.center 

    gunPosX = rotateAroundCircleX(playerRect,Tangle_radians,30)
    gunPosY = rotateAroundCircleY(playerRect,Tangle_radians,30)

    gunRect.x = gunPosX
    gunRect.y = gunPosY

    guns.blitPlayer(playerSprites,M_pressed,Tangle_degrees,playerRect,current_frame)
    playerMask = pygame.mask.from_surface(guns.returnPlayerSurface())

    deleteIndex = []

    if guns.canShoot(current_frame, fireRate, M_pressed):
        bulletObject = bulletLogic(gunPosX, gunPosY, TrotX, TrotY, recoil, Tdist, Tangle_degrees, bulletSpeed)
        bulletObject.GetRoation()
        bulletObject.SpawnBullet()
        bulletList.append(bulletObject)
        pygame.mixer.Sound.play(ravagerShot)

    # In your game loop:
    for x in range(len(bulletList)):
        bullet = bulletList[x]
        bullet.MoveBullet()
        if (bullet.DeleteBullet()):
            deleteIndex.append(x)

    for index in sorted(deleteIndex):
            del bulletList[index]

    if (current_frame % 30 == 0):
        gargoyleX = random.randint(0,1000)
        gargoyleList.append(Gargoyle(gargoyleX,gargoyleY,playerRect,gargoyleSpeed,current_frame,playerMask,gargoyleHealth,bulletDamage,bulletMask,bulletX,bulletY))

    if (current_frame % 660 == 0):
        bruteX = random.randint(0,1000)
        bruteList.append(Brute(bruteX,bruteY,playerRect,bruteSpeed,current_frame,playerMask,bruteHealth,bulletDamage,bulletMask,bulletX,bulletY,bruteWindUpCooldown,bruteAttackCooldown))

    enemyKilledIndex = []

    for x in range(len(gargoyleList)):
        enemy = gargoyleList[x]
        enemy.moveEnemy(playerPathFindRect, gargoyleSpeed, current_frame)
        enemy.detectPlayerHit(playerMask, playerRect)
        enemy.getDistanceFromPlayer(playerRect)
        enemy.getEnemyState(current_frame)
        enemy.scaleEnemyRect(0.5)

        killedIndex = logic.killEnemy(bulletList,enemy,bulletDamage,gargoyleDeath,x)
        enemyKilledIndex.extend(killedIndex)
        logic.enemyBulletCollision(bulletList,bulletHit,enemy)

    for index in sorted(enemyKilledIndex, reverse=True):
        del gargoyleList[index]

    bruteKilledIndex = []

    for x in range(len(bruteList)):
        brute = bruteList[x]
        brute.chargeAttack(playerPathFindRect, gargoyleSpeed, current_frame)
        brute.detectPlayerHit(playerMask, playerRect)
        brute.getDistanceFromPlayer(playerRect)
        brute.scaleEnemyRect(0.5)
        brute.getEnemyState(current_frame)

        killedIndex = logic.killEnemy(bulletList,brute,bulletDamage,gargoyleDeath,x)
        bruteKilledIndex.extend(killedIndex)
        logic.enemyBulletCollision(bulletList,bulletHit,brute)

    for index in sorted(bruteKilledIndex, reverse=True):
        del bruteList[index]

    #screen.blit(testSurface,(gunPosX,gunPosY))
    #screen.blit(rotated_player_image, playerRoatedRect.topleft)

    pygame.display.update()
    clock.tick(60)