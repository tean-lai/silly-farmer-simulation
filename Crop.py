import pygame as game

import FarmerVars as Vars

from random import random

seedSprites = {}  # contains the names of the sprite files
grownSprites = {}

for i in range(4):
    seedSprites[i] = "seed" + Vars.plantTypes[i]
    grownSprites[i] = "grown" + Vars.plantTypes[i]


class Crop:
    """
    buy price
    sell price
    grow time
    nutrition value
    chance to fail

    5 crops:
    1, 100, 10
    1, 0, 5
    0, 0, 20
    0, 0, 2
    0, 0, 100
    """

    def __init__(self, type, farmNum, tile=None, r=None, c=None):  # add in type later
        self.farmNum = farmNum
        self.farmer = Vars.farmerList[self.farmNum]
        self.grid = Vars.farmGrid[self.farmNum]
        
        self.stage = Vars.stages[0]
        self.stageNum = 0
        self.failed = False
        
        self.type = type
        self.info = Vars.info[self.type]
        
        self.sprite = game.image.load(seedSprites[self.type] + ".png")
        self.sprite = game.transform.scale(self.sprite, (Vars.PLOT_SIZE, Vars.PLOT_SIZE))
        self.spriteRect = self.sprite.get_rect()
        self.spriteRect.left = -1000  # !!!!!!!!
        self.spriteRect.top = -1000  # !!!!!!!
        # self.y = (r + Vars.NUM_SQUARES - Vars.NUM_PLOT) * Vars.PLOT_SIZE
        
        if r and c:
            self.setCoord(r, c)
        else:
            self.r = 0
            self.c = 0
            
        self.tile = tile
        
        self.info = Vars.info[type]
        
        self.failChecked = False # !!!!

        self.ticksAlive = 0

    def update(self, screen):  # also update
        if Vars.farmerList[self.farmNum].grid[self.r][self.c].type != "store":  # so it doesn't draw on store tiles
            self.ticksAlive += 1
            if self.ticksAlive == self.info[2] * Vars.TICKS_PER_DAY and self.stage != Vars.stages[-1] and not self.failChecked:  # when it grows it must get new sprites
                self.stageNum += 1
                self.stage = Vars.stages[self.stageNum]
                self.sprite = game.image.load(grownSprites[self.type] + ".png")
                self.sprite = game.transform.scale(self.sprite, (Vars.PLOT_SIZE, Vars.PLOT_SIZE))
                self.spriteRect = self.sprite.get_rect()
                self.spriteRect.left = self.c * Vars.PLOT_SIZE
                self.spriteRect.top = self.r * Vars.PLOT_SIZE
                if self.farmNum == 1 or self.farmNum == 3:
                    self.spriteRect.left += Vars.PLOT_SIZE * Vars.NUM_SQUARES
                if self.farmNum == 2 or self.farmNum == 3:
                    self.spriteRect.top += Vars.PLOT_SIZE * Vars.NUM_SQUARES
                    
            if self.stage == Vars.stages[-1] and not self.failChecked: # !!!!!!!
                if random()*100 < self.info[4] / self.tile.multiplier:
                    self.failed = True
                    self.sprite = game.image.load("failed.png")
                    self.sprite = game.transform.scale(self.sprite, (Vars.PLOT_SIZE, Vars.PLOT_SIZE))
                    self.spriteRect = self.sprite.get_rect()
                    self.spriteRect.left = self.c * Vars.PLOT_SIZE
                    self.spriteRect.top = self.r * Vars.PLOT_SIZE
                    if self.farmNum == 1 or self.farmNum == 3:
                        self.spriteRect.left += Vars.PLOT_SIZE * Vars.NUM_SQUARES
                    if self.farmNum == 2 or self.farmNum == 3:
                        self.spriteRect.top += Vars.PLOT_SIZE * Vars.NUM_SQUARES
                
                self.tile.nutrition += self.info[3]
                if self.tile.nutrition < 1:
                    self.tile.nutrition = 1
                elif self.tile.nutrition > 100:
                    self.tile.nutrition = 100
                self.failChecked = True

            screen.blit(self.sprite, self.spriteRect)

    def setCoord(self, r, c):  # updates coordinates and sprite rec location
        self.r = r
        self.c = c
        self.spriteRect.left = c * Vars.PLOT_SIZE
        self.spriteRect.top = r * Vars.PLOT_SIZE
        if self.farmNum == 1 or self.farmNum == 3:
            self.spriteRect.left += Vars.PLOT_SIZE * Vars.NUM_SQUARES
        if self.farmNum == 2 or self.farmNum == 3:
            self.spriteRect.top += Vars.PLOT_SIZE * Vars.NUM_SQUARES
