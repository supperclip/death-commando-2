import pygame
import sys
from pygame.locals import QUIT
import random
import math
from enum import Enum

from gun_class import gunLogic
from gun_class import bulletLogic

from player_class import player
from player_class import Directions

from enemy_class import EnemyLogic
from enemy_class import States
from enemy_class import Gargoyle
from enemy_class import Brute
from enemy_class import Rager

from gameLogic_class import gameLogic

class gunState(Enum):
    notFiring = 0
    Firing = 1
    Reloading = 2

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("death commando: pest control II")
clock = pygame.time.Clock()

basicFont = pygame.font.Font("fonts/Swiss 721 Extended Bold.otf", 50)
pixelFont = pygame.font.Font("fonts/dogicapixel.ttf", 40)
pixelFontBold = pygame.font.Font("fonts/dogicapixelbold.ttf", 50)

BLACK = (0,0,0)
WHITE = (255,255,255)

background = pygame.image.load("x/background.png")

current_frame = 0
Tangle_degrees = 0

testSurface = pygame.Surface((20,20))
testSurface.fill("black")

magSizeUI = pygame.Surface((70,92))
magSizeUI.fill("white")

playerPathFindRect = pygame.surface.Surface((45,45))
playerPathFindRect = playerPathFindRect.get_rect()

UITest = pygame.Surface((210,100))
UITest.fill("black")

UI1 = pygame.image.load("x/ammoUI.png")
UI1 = pygame.transform.scale_by(UI1 ,(2.7,2.2))

player_1 = pygame.image.load("x/player_1.png")
player_1 = pygame.transform.rotate(player_1, 90)
playerRect = player_1.get_rect()

playerShoot1 = pygame.image.load("x/player_shoot_1.png")
playerShoot1 = pygame.transform.rotate(playerShoot1, 90)

playerShoot2 = pygame.image.load("x/player_shoot_2.png")
playerShoot2 = pygame.transform.rotate(playerShoot2, 90)

playerShoot3 = pygame.image.load("x/player_shoot_3.png")
playerShoot3 = pygame.transform.rotate(playerShoot3, 90)

playerFlex1 = pygame.image.load("x/player_FLEX_1.png")
playerFlex1 = pygame.transform.rotate(playerFlex1, 90)

playerFlexShoot1 = pygame.image.load("x/player_FLEX_shoot1.png")
playerFlexShoot1 = pygame.transform.rotate(playerFlexShoot1, 90)

playerFlexShoot2 = pygame.image.load("x/player_FLEX_shoot2.png")
playerFlexShoot2 = pygame.transform.rotate(playerFlexShoot2, 90)

playerFlexShoot3 = pygame.image.load("x/player_FLEX_shoot3.png")
playerFlexShoot3 = pygame.transform.rotate(playerFlexShoot3, 90)

playerSmartRifle = pygame.image.load("x/player_SmartRifle.png")
playerSmartRifle = pygame.transform.rotate(playerSmartRifle, 90)

playerSmartRifleShoot1 = pygame.image.load("x/player_SmartRifle_shoot_1.png")
playerSmartRifleShoot1 = pygame.transform.rotate(playerSmartRifle, 90)

playerSmartRifleShoot2 = pygame.image.load("x/player_SmartRifle_shoot_2.png")
playerSmartRifleShoot2 = pygame.transform.rotate(playerSmartRifleShoot2, 90)

playerSmartRifleShoot3 = pygame.image.load("x/player_SmartRifle_shoot_3.png")
playerSmartRifleShoot3 = pygame.transform.rotate(playerSmartRifleShoot3, 90)

bullet1 = pygame.image.load("x/bullet1.png")
bulletMask = pygame.mask.from_surface(bullet1)

FLEXList = [playerFlex1,playerFlexShoot1,playerFlexShoot2,playerFlexShoot3]
ravagerMK1List = [player_1,playerShoot1,playerShoot2,playerShoot3]
SmartRifleList = [playerSmartRifle,playerSmartRifleShoot1,playerSmartRifleShoot2,playerSmartRifleShoot3]

ravagerShell = pygame.image.load("x/ravagerShell.png")

bullet1 = pygame.image.load("x/bullet1.png")

playerSprites = ravagerMK1List

#sounds
bulletHit = pygame.mixer.Sound("sounds/bulletImpact.wav")
bulletHit.set_volume(0.1)

ravagerShoot = pygame.mixer.Sound("sounds/rifleShot.wav")
ravagerShoot.set_volume(4)

flexShoot = pygame.mixer.Sound("sounds/flexShoot.wav")
flexShoot.set_volume(0.7)

reload1 = pygame.mixer.Sound("sounds/metalReload1.wav")
reload2 = pygame.mixer.Sound("sounds/metalReload2.wav")
reload3 = pygame.mixer.Sound("sounds/metalReload3.wav")

#player data
Current_Direction = Directions.InValid
MoveSpeed = 1.2
Tangle_radians = 0

M_pressed = False
R_pressed = False

animationList = ravagerMK1List

playerMask = pygame.mask.from_surface(player_1)

#gun data:
bulletList = []
weaponShoot = ravagerShoot

bulletSpeed = 7.5
fireRate = 15
bulletDamage = 15
recoil = 45
lineEnd = 0

magSizeUIHeight = 92

mags = 5
maxMags = 5
magText = pixelFont.render(str(mags) + "/" + str(maxMags),True,WHITE)

magUI = pygame.image.load("x/magUI.png") #24 * 42
magUI = pygame.transform.scale(magUI,((24 * 2),(42 * 2)))

maxMagSize = 20
magSize = maxMagSize

autoOfAmmo = False

currentGunState = gunState.notFiring

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

#corsshair
crosshair = pygame.image.load("x/crosshair.png")
crosshair = pygame.transform.scale(crosshair, (35, 35))
cursor = pygame.cursors.Cursor((17,17), crosshair)
pygame.mouse.set_cursor(cursor)

#Gargoyle data:
gargoyleX = random.randint(0,1000)
gargoyleY = 0
gargoyleSpeed = 1.8
gargoyleHealth = 15
gargoyleList = []
gargoyleDeath = pygame.mixer.Sound("sounds/enemy3.wav")
gargoyleDeath.set_volume(2.5)

#brute data
bruteX = random.randint(0,1000)
bruteY = 0
bruteSpeed = 1
bruteHealth = 200
bruteWindUpCooldown = 40
bruteAttackCooldown = 90
bruteList = []

#rager data
ragerX = random.randint(0,1000)
ragerY = 0 
ragerSpeed = 4
ragerHealth = 5
ragerList = []

bullet1 = pygame.image.load("x/bullet1.png")

guns = gunLogic(M_pressed,gunRect,bulletSpeed,current_frame,fireRate,Tangle_degrees,lineEnd,Tangle_radians,TrotX,TrotY,Tdist,recoil,animationList)

p = player(Current_Direction,current_frame,MoveSpeed)
logic = gameLogic()


def rotateAroundCircleX(rect,angle,radius):
    x = rect.x + 50 + math.cos(-angle - 0.25) * radius
    return x

def rotateAroundCircleY(rect,angle,radius):
    y = rect.y + 50 - math.sin(-angle - 0.25) * radius
    return y

WeaponSwap = False
def GunFunction(gun):
    if (gun == "FLEX raider MK1"):
        return [1,6,5,1,FLEXList,45,7,flexShoot] #bulletSpeed,fireRate,bulletDamage,recoil,animations,mags
    if (gun == "ravagerMK1"):
        return [7.5,15,20,45,ravagerMK1List,20,5,ravagerShoot] #bulletSpeed,fireRate,bulletDamage,recoil,animations,mags
    if (gun == "MK1SmartRifle"):
        return [5,10,15,0,SmartRifleList,15,5,ravagerShoot] #bulletSpeed,fireRate,bulletDamage,recoil,animations,magSize,mags
    
def Delay(inputFrame,frame,delay):
    if (inputFrame == (frame + delay)):
        return True
    else:
        return False
    
enemyTypes = 3

while True:
    
    current_frame += 1
    
    screen.blit(background, (0, 0))

    magSizeUI.fill("white")
    screen.blit(magSizeUI,(925,(590 - magSizeUIHeight) + 75))
    screen.blit(UI1,(774,566))
    screen.blit(magText,(810,605))

    magText = pixelFont.render(str(mags) + "/" + str(maxMags),True,WHITE)

    if (WeaponSwap):
        weaponData = GunFunction(currentGun)
        bulletSpeed = weaponData[0]
        fireRate = weaponData[1]
        bulletDamage = weaponData[2]
        recoil = weaponData[3]
        animationList = weaponData[4]
        maxMagSize = weaponData[5]
        magSize = weaponData[5]
        mags = weaponData[6]
        maxMags = weaponData[6]
        weaponShoot = weaponData[7]
        WeaponSwap = False
    
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

    if keys[pygame.K_r]:
        R_pressed = True

    if keys[pygame.K_1]:
        currentGun = "FLEX raider MK1"
        WeaponSwap = True
    if keys[pygame.K_2]:
        currentGun = "MK1SmartRifle"
        WeaponSwap = True

    if not(autoOfAmmo) and (M_pressed):
        currentGunState = gunState.Firing
    if not (M_pressed):
        currentGunState = gunState.notFiring
    if (autoOfAmmo) or (R_pressed):
        currentGunState = gunState.Reloading

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

    guns.blitPlayer(animationList,M_pressed,Tangle_degrees,playerRect,current_frame,currentGunState)
    
    if(guns.reloadGun(current_frame,currentGunState,reload1,reload2,reload3)):
        magSize = maxMagSize
        R_pressed = False
        magSizeUIHeight = (92 * (magSize / maxMagSize))
        magSizeUI = pygame.transform.scale(magSizeUI,(70,magSizeUIHeight))

    playerMask = pygame.mask.from_surface(guns.returnPlayerSurface())

    if (magSize <= 0):
        autoOfAmmo = True
    else:
        autoOfAmmo = False

    if guns.canShoot(current_frame, fireRate,currentGunState):
        if (currentGun == "MK1SmartRifle"):
            if (len(gargoyleList) > 0):
                gargoyle = gargoyleList[random.randint(0,(len(gargoyleList) - 1))]
                enemyTarget = [gargoyle.X,gargoyle.Y]
                enemyTargetX = mouse_x - enemyTarget[0]
                enemyTargetY = mouse_y - enemyTarget[1]
                bulletObject = bulletLogic(gunPosX, gunPosY, enemyTargetX, enemyTargetY, recoil, Tdist, Tangle_degrees, bulletSpeed)
                bulletObject.GetRoation()
                bulletObject.SpawnBullet()
                bulletList.append(bulletObject)
                pygame.mixer.Sound.play(weaponShoot)
                magSize -= 1
                magSizeUIHeight = (92 * (magSize / maxMagSize))
                magSizeUI = pygame.transform.scale(magSizeUI,(70,magSizeUIHeight))
        else:
            bulletObject = bulletLogic(gunPosX, gunPosY, TrotX, TrotY, recoil, Tdist, Tangle_degrees, bulletSpeed)
            bulletObject.GetRoation()
            bulletObject.SpawnBullet()
            bulletList.append(bulletObject)
            pygame.mixer.Sound.play(weaponShoot)
            magSize -= 1
            magSizeUIHeight = (92 * (magSize / maxMagSize))
            magSizeUI = pygame.transform.scale(magSizeUI,(70,magSizeUIHeight))



    for x in range(len(bulletList)):
        bullet = bulletList[x]
        bullet.MoveBullet()

    if (current_frame % 30 == 0):
        gargoyleX = random.randint(0,1000)
        gargoyleList.append(Gargoyle(gargoyleX,gargoyleY,playerRect,gargoyleSpeed,current_frame,playerMask,gargoyleHealth,bulletDamage,bulletMask,bulletX,bulletY))

    if (current_frame % 660 == 0):
        bruteX = random.randint(0,1000)
        bruteList.append(Brute(bruteX,bruteY,playerRect,bruteSpeed,current_frame,playerMask,bruteHealth,bulletDamage,bulletMask,bulletX,bulletY,bruteWindUpCooldown,bruteAttackCooldown))

    if (current_frame % 250 == 0):
        for x in range(2):
            ragerX = random.randint(0,1000)
            ragerList.append(Rager(ragerX,ragerY,playerRect,ragerSpeed,current_frame,playerMask,ragerHealth,bulletDamage,bulletMask,bulletX,bulletY))

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
        brute.chargeAttack(playerPathFindRect, bruteSpeed, current_frame)
        brute.detectPlayerHit(playerMask, playerRect)
        brute.getDistanceFromPlayer(playerRect)
        brute.scaleEnemyRect(0.5)
        brute.getEnemyState(current_frame)

        killedIndex = logic.killEnemy(bulletList,brute,bulletDamage,gargoyleDeath,x)
        bruteKilledIndex.extend(killedIndex)
        logic.enemyBulletCollision(bulletList,bulletHit,brute)

    for index in sorted(bruteKilledIndex, reverse=True):
        del bruteList[index]

    ragerKilledIndex = []

    for x in range(len(ragerList)):
        rager = ragerList[x]
        rager.moveEnemy(playerPathFindRect, ragerSpeed, current_frame)
        rager.detectPlayerHit(playerMask, playerRect)
        rager.getDistanceFromPlayer(playerRect)
        rager.getEnemyState(current_frame)
        rager.scaleEnemyRect(0.5)

        killedIndex = logic.killEnemy(bulletList,rager,bulletDamage,gargoyleDeath,x)
        ragerKilledIndex.extend(killedIndex)
        logic.enemyBulletCollision(bulletList,bulletHit,rager)

    for index in sorted(ragerKilledIndex, reverse=True):
        del ragerList[index]

    #screen.blit(testSurface,(gunPosX,gunPosY))
    #screen.blit(rotated_player_image, playerRoatedRect.topleft)

    pygame.display.update()
    clock.tick(60)