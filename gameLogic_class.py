import pygame
import sys
from pygame.locals import QUIT
import math
import random


class gameLogic:
        
    def enemyBulletCollision(self,bulletList,bulletHit,enemy):
            
        for y in range(len(bulletList)):
            bullet = bulletList[y]

            if bullet.CheckEnemyHit(enemy.rect):
                pygame.mixer.Sound.play(bulletHit)
                return bulletList.pop(y)
            
    def killEnemy(self, bulletList, enemy, bulletDamage, deathSound, currentIndex):
        for y in range(len(bulletList)):
            bullet = bulletList[y]
            enemy.getEnemyHP(bulletDamage, bullet.bulletRect)

        if enemy.enemyHP <= 0:
            pygame.mixer.Sound.play(deathSound)
            return [currentIndex]
        return []
