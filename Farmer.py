import pygame as game

import FarmerVars as Vars
import Crop
from random import randint, shuffle, choice

# replace the whole thing

farmerLayer = 1
barnCoord = (0,0)
plant1 = (1,7) # medium
plant2 = (3,7) # nutritional
plant3 = (5,7) # pricey
plant4 = (7,7) # cheap

travelDict = {
    0: plant1,
    1: plant2,
    2: plant3,
    3: plant4,
    }

class Farmer:

    def __init__(self, farmerType, farm, screen, x, y):

        self.farmerType = farmerType  # Greedy, control, eco-friendly, efficient etc.
        self.farm = farm  # Which one of the four farms it occupies

        self.grid = Vars.farmGrid[self.farm]
        self.grid[y][x].layers[1] = self # !!!! monky lmao
        
        if self.farmerType != "control":
            self.queue = []
            self.args = []
        
        if self.farmerType == "control":
            self.sprite = game.image.load("farmerMario.png")

        if self.farmerType == "eco":
            self.sprite = game.image.load("FarmerEco.png")
            self.profitMin = [0,0,0,0]
            self.order = [1,2,0,3]
        
        if self.farmerType == "effi":
            self.sprite = game.image.load("FarmerMario.png")
            self.profitMin = [300,6,8000,25]
            self.order = [2,1,0,3]
        
        if self.farmerType == "greedy":
            self.sprite = game.image.load("FarmerGreedy.png")
            self.profitMin = [290,1,8000,20]
            self.order = [2,0,3,1]
            
        if self.farmerType == "monkey":
            self.MONKEYMODE = [self.restFull,self.sellAllMove,self.plantNext,self.harvestNext,self.buyAllMove,self.moveRest]
            self.sprite = game.image.load("MonkeyFarmer.png")
            self.profitMin = [0,0,0,0]
            for i in range(4):
                self.profitMin[i] = randint(Vars.info[i][1]-Vars.deviationMaxes[i][1], Vars.info[i][1]+Vars.deviationMaxes[i][1])
            self.order = [0,1,2,3]
            shuffle(self.order)

        self.sprite = game.transform.scale(self.sprite, (Vars.PLOT_SIZE, Vars.PLOT_SIZE))
        self.spriteRect = self.sprite.get_rect()

        self.x = x
        self.y = y
        self.xShift = 0
        self.yShift = 0
        
        if self.farm == 1 or self.farm == 3:  # shifted so the tiles will draw on separate
            self.xShift += Vars.PLOT_SIZE * Vars.NUM_SQUARES  # areas on the screen and not all on top
        if self.farm == 2 or self.farm == 3:  # of each other
            self.yShift += Vars.PLOT_SIZE * Vars.NUM_SQUARES

        '''
        Less "necessary" commands, for the "simulation"
        '''

        self.happiness = 100
        self.inv = []
        self.money = 10  # starting balance
        self.sinceLastWait = 0
        self.nutritionExpect = 4
        self.action = "None"

    def update(self, screen):

        # if self.farm == 0:  # made this 0 cuz it makes more sense for the first farm to be farm 0

        self.spriteRect.left = (self.x) * Vars.PLOT_SIZE + self.xShift
        self.spriteRect.top = (self.y) * Vars.PLOT_SIZE + self.yShift

        screen.blit(self.sprite, self.spriteRect)

    '''
    TIER 3 COMMANDS, WE IN IT NOW BOYS
    '''

#     def harvestAll(self):
#         
#         for r in range(len(self.grid)):
#             for c in range(len(self.grid[0])):
#                 if self.grid[r][c].layers[0] and self.grid[r][c].type == 'farmland':
#                     if self.grid[r][c].layers[0].stage == "fully grown":
#                         self.moveTo((r,c))
#                         self.queue.append(self.pickUp)
                        
    def harvestNext(self):
        
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c].layers[0] and self.grid[r][c].type == 'farmland':
                    if self.grid[r][c].layers[0].stage == "fully grown":
                        self.moveTo((r,c))
                        self.queue.append(self.pickUp)
                        return
                
#     def plantAll(self):
#         
#         for i in range(self.toPlant):
#             self.searchNutrition = 4
#             self.plantNext()
    
    def plantNext(self):
        
        i = 0
        tempInv = []
        while i < len(self.inv):
            if self.inv[i].stage == "fully grown":
                tempInv.append(self.inv[i])
                del self.inv[i]
            else:
                i += 1
        self.inv += tempInv
        
        if self.seedInInv != 0:
            if self.inv[0].type == 1:
                for r in range(len(self.grid)):
                    for c in range(len(self.grid[0])):
                        if not self.grid[r][c].layers[0] and self.grid[r][c].type == "farmland":
                            if self.grid[r][c].nutritionLevel != 4:
                                self.moveTo((r,c))
                                self.queue.append(self.plantFirst)
                                self.seedInInv -= 1
                                return
                if not self.queue:
                    for r in range(len(self.grid)):
                        for c in range(len(self.grid[0])):
                            
                            if not self.grid[r][c].layers[0] and self.grid[r][c].type == "farmland" and self.grid[r][c].nutritionLevel == self.searchNutrition:
                                #print(self.grid[r][c].nutritionLevel, self.searchNutrition)
                                self.moveTo((r,c))
                                self.queue.append(self.plantFirst)
                                self.seedInInv -= 1
                                return
            else:
                for r in range(len(self.grid)):
                    for c in range(len(self.grid[0])):
                        
                        if not self.grid[r][c].layers[0] and self.grid[r][c].type == "farmland" and self.grid[r][c].nutritionLevel == self.searchNutrition:
                            #print(self.grid[r][c].nutritionLevel, self.searchNutrition)
                            self.moveTo((r,c))
                            self.queue.append(self.plantFirst)
                            self.seedInInv -= 1
                            return
                    
            self.searchNutrition -= 1
            self.plantNext()
        else:
            return
        
    '''
    These are the tier 2 commands. They don't directly add to queue, but add tier 1 commands to queue for processing
    '''
    
    def buyAllMove(self):
        
        for i in range(4):
            which = self.order[i]
            if self.plantOptions[which]:
                self.moveTo(travelDict[which])
                self.queue.append(self.buy)
                self.args.append([self.plantOptions[which]])
                
    def buy(self,amt):
        
        if self.grid[self.y][self.x].type == "store":
            for i in range(amt):
                self.pickUp()
    
    def moveRest(self):
        
        self.moveTo(barnCoord)
        self.queue.append(self.rest)
        
    def restFull(self):
        
        self.moveTo(barnCoord)
        tempHappiness = self.happiness
        while tempHappiness < 100:
            self.queue.append(self.rest)
            tempHappiness += Vars.restAmt
        
    def sellAllMove(self):
        
        self.moveTo(barnCoord)
        self.queue.append(self.sellAll)
                            
    def moveTo(self, target):
        
        xDiff = target[1] - self.tempx
        yDiff = target[0] - self.tempy
        
        while xDiff != 0 or yDiff != 0:
            if abs(xDiff) > abs(yDiff):
                if xDiff < 0:
                    self.queue.append(self.moveLeft)
                    self.tempx -= 1
                elif xDiff > 0:
                    self.queue.append(self.moveRight)
                    self.tempx += 1
            elif abs(xDiff) <= abs(yDiff):
                if yDiff < 0:
                    self.queue.append(self.moveUp)
                    self.tempy -= 1
                elif yDiff > 0:
                    self.queue.append(self.moveDown)
                    self.tempy += 1
            xDiff = target[1] - self.tempx
            yDiff = target[0] - self.tempy
                    

        
    '''
    all the things that the AI can do; omega basic, tier 1 action
    '''
    
    def wait(self):

        pass
    
    def rest(self):        
        
        if self.grid[self.y][self.x].type == "barn":
            self.happiness += Vars.restAmt
            if self.happiness > 100:
                self.happiness = 100
    
    def sellAll(self):
        
        self.inv = list(filter(lambda i: self.putDown(i, 0), self.inv))
        
    def plantFirst(self):

        if not self.grid[self.y][self.x].layers[0] and self.grid[self.y][self.x].type == 'farmland':
            
            for i in self.inv:

                if i.stage == "seed":
                    self.putDown(i, 1)
                    break
                
    def buyAll(self):
        
        bought = 0
        if self.grid[self.y][self.x].type == "store":
            while self.money >= self.grid[self.y][self.x].layers[0].info[0] and bought < self.toPlant:
                
                bought += 1
                self.pickUp()

    def moveUp(self):
        
        try:
            if self.y > 0:
                self.grid[self.y - 1][self.x].layers[farmerLayer] = self
                self.grid[self.y][self.x].layers[farmerLayer] = 0
                self.y -= 1

        except IndexError:
            pass
        
    def moveDown(self):
        
        try:

            self.grid[self.y + 1][self.x].layers[farmerLayer] = self
            self.grid[self.y][self.x].layers[farmerLayer] = 0
            self.y += 1

        except IndexError:
            pass
        
    def moveLeft(self):
        
        try:

            if self.x > 0:
                self.grid[self.y][self.x - 1].layers[farmerLayer] = self
                self.grid[self.y][self.x].layers[farmerLayer] = 0
                self.x -= 1

        except IndexError:
            pass
        
    def moveRight(self):
        
        try:

            self.grid[self.y][self.x + 1].layers[farmerLayer] = self
            self.grid[self.y][self.x].layers[farmerLayer] = 0
            self.x += 1

        except IndexError:
            pass
        
    def pickUp(self):

        # if self.grid[self.y][self.x].layers[0]:
        #     self.inv.append(self.grid[self.y][self.x].layers[0])
        # if self.grid[self.y][self.x].type != "store":
        #     self.grid[self.y][self.x].layers[0] = 0
        obj = self.grid[self.y][self.x].layers[0]  # !!!!!
        if obj:  # to make sure that farmer doesn't pick up 0's !!!!1
            if self.grid[self.y][self.x].type == "farmland" and obj.stage == "fully grown":
                self.inv.append(obj)
            elif self.grid[self.y][self.x].type == "store":
                self.inv.append(Crop.Crop(obj.type, self.farm))  # !!!!!

        if self.grid[self.y][self.x].type == "store":
            self.money -= self.grid[self.y][self.x].layers[0].info[0]  # takes money from farmer's account
            if self.money < 0:
                self.money += self.grid[self.y][self.x].layers[0].info[0]  # return money to account
                self.inv.pop()  # remove it from his inv
        else:
            self.grid[self.y][self.x].layers[0] = 0  # so the store doesn't get depleted of crops


    def putDown(self, obj, mode):

        # if not self.grid[self.y][self.x].layers[0]:

            # for i in range(len(self.inv)):
                # if isinstance(self.inv[i], obj):
                # if self.inv[i] == obj:  # !!!!!!
                #     self.grid[self.y][self.x].layers[0] = self.inv.pop(i)
                #     obj.set_coord(self.y, self.x)  # give the plant new coordinates
                #     break

        if mode == 0:
            if obj.stage == "fully grown":
                if Vars.info[obj.type][1] <= self.profitMin[obj.type]:
                    return True
                if obj.failed == False:
                    obj.farmer.money += obj.info[1]
                return False
            return True
        elif mode == 1:
            self.grid[self.y][self.x].layers[0] = obj
            self.inv.remove(obj)
            obj.setCoord(self.y, self.x)
            obj.tile = self.grid[self.y][self.x]
    
    def shouldSell(self):
        
        for i in range(len(self.inv)):
            if self.inv[i].info[1] >= self.profitMin[i]:
                return True
        return False
    
    def getInfo(self):
        
        available = 0
        seedInInv = 0
        readyForHarvest = 0
        searchNutrition = 0
        
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c].type == "farmland":
                    if self.grid[r][c].nutritionLevel > searchNutrition:
                        searchNutrition = self.grid[r][c].nutritionLevel
                    if not self.grid[r][c].layers[0]:
                        available += 1
                    elif self.grid[r][c].layers[0].stage == "fully grown":
                        readyForHarvest += 1
                
                    
        for item in self.inv:
            if item.stage == "seed":
                seedInInv += 1
                    
        return available, seedInInv, available-seedInInv, readyForHarvest, searchNutrition
                    
    '''
    ALL THE MOVE FUNCTION HAHAHAHAHHA
    '''
   
    def move(self, keyVal=None):

        if self.farmerType == "control":
            
            self.controlMove(keyVal)
            
        if self.farmerType != "control":
             
            for i,threshold in enumerate(Vars.happinessThreshold):
                if self.happiness > threshold:
                    self.waitMod = Vars.happinessTimers[i]
                    break
        if self.farmerType == "effi":
            
            self.effiMove()
            
        if self.farmerType == "eco":
    
            self.ecoMove()
            
        if self.farmerType == "greedy":
            
            self.greedyMove()
            
        if self.farmerType == "monkey":
            
            self.monkeyMove()
    
    '''
    control movements
    '''
    def controlMove(self, keyVal):

        if keyVal == game.K_d or keyVal == game.K_RIGHT:

            self.moveRight()

        if keyVal == game.K_a or keyVal == game.K_LEFT:

            self.moveLeft()

        if keyVal == game.K_s or keyVal == game.K_DOWN:

            self.moveDown()

        if keyVal == game.K_w or keyVal == game.K_UP:

            self.moveUp()

        if keyVal == game.K_q:
            
            self.pickUp()

        if keyVal == game.K_e:

            if self.grid[self.y][self.x].type == 'barn':
                
                self.sellAll()

            if self.grid[self.y][self.x].type == 'farmland':
                
                self.plantFirst()
    
    '''
    monkey-specific functions
    '''
        
    def monkeyBestPlant(self,numNeedNutrition):
        
        chose = 0
        tempBalance = self.money
        tempNeedNutrition = numNeedNutrition
        
        plantOptions = [0,0,0,0]
        profitRatios = [0,0,0,0]
        
        for i in range(4):
            profitRatios[i]= Vars.info[i][1]/Vars.info[i][0]
        
        profitRatios[2] *= randint(0,50) * .1
        profitRatios[3] *= randint(0,25) * .1
        
#         print(profitRatios,"profits")
        
        while chose < self.toPlant:
            
            chose += 1
            
            if tempNeedNutrition > 0 and tempBalance >= Vars.info[1][0]:
                plantOptions[1] += 1
                tempBalance -= Vars.info[1][0]
                tempNeedNutrition -= 1
            
            elif tempBalance >= Vars.info[2][0] and profitRatios[2] > profitRatios[0] and profitRatios[2] > profitRatios[3]:
                plantOptions[2] += 1
                tempBalance -= Vars.info [2][0]
                
            elif tempBalance >= Vars.info[0][0] and profitRatios[0] > profitRatios[3]:
                plantOptions[0] += 1
                tempBalance -= Vars.info [0][0]
                
            elif tempBalance >= Vars.info[3][0]:
                plantOptions[3] += 1
                tempBalance -= Vars.info [3][0]
                
            else:
                return plantOptions
        return plantOptions
    
    def monkeyInfo(self):
    
        numNeedNutrition = 0
        
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c].type == "farmland":
                    try:
                        if self.grid[r][c].nutritionLevel < randint(0,4) and self.grid[r][c].layers[0].type != 1:
                            numNeedNutrition += 1
                    except AttributeError:
                        if self.grid[r][c].nutritionLevel < randint(0,4):
                            numNeedNutrition += 1
        
        plantOptions = self.effiBestPlant(numNeedNutrition)
        
        return numNeedNutrition, plantOptions
    
    def monkeyMove(self):
        
        if self.money > Vars.winCondition and Vars.winner == False:
            self.isWinner = True
            Vars.winner = Vars.farmerNames[self.farmerType] + "Farmer"
        
        if self.queue:
            
            self.sinceLastWait += 1
            if self.waitMod != 0 and self.sinceLastWait % self.waitMod == 0:
                self.sinceLastWait = 0
                self.wait()
            else:
                try:
                    self.queue[0]()
                    
                except TypeError:
                    try:
                        self.queue[0](*self.args[0])
                        del self.args[0]
                    except IndexError:
                        pass
                del self.queue[0]
        else:
            
            self.tempx, self.tempy = self.x, self.y
            
            self.available,self.seedInInv,self.toPlant,self.readyForHarvest,self.searchNutrition = self.getInfo()
            self.numNeedNutrition, self.plantOptions = self.monkeyInfo()
            
            for i in range(4):
                self.profitMin[i] = randint(Vars.info[i][1]-Vars.deviationMaxes[i][1], Vars.info[i][1]+Vars.deviationMaxes[i][1])
                
            #print(self.plantOptions)
            
            if self.happiness < 50:
                self.action = "resting"
                self.restFull()
                self.sellAllMove()
                             
            elif any(item.stage == 'seed' for item in self.inv) and self.available > 0:
                self.action = "planting"
                self.plantNext()
                
            elif self.readyForHarvest != 0:
                self.action = "harvesting"
                self.harvestNext()
            
            elif self.money > 0 and self.toPlant > 0:
                self.action = "buying"
                self.buyAllMove()
                                   
            elif any(item.stage == 'fully grown' for item in self.inv) and self.shouldSell():
                self.action = "selling"
                self.sellAllMove()
                
            else:
                self.action = "None; resting"
                self.moveRest()
                
    '''
    greedy-specific functions
    '''
    
    def greedyBestPlant(self,nutritionValueMult):
        
        chose = 0
        tempBalance = self.money
        
        plantOptions = [0,0,0,0]
        profitRatios = [0,0,0,0]
        
        for i in range(4):
            profitRatios[i]= Vars.info[i][1]/Vars.info[i][0]
        
        profitRatios[2] *= 2 * nutritionValueMult
        profitRatios[3] *= .2 * nutritionValueMult
        profitRatios[0] *= nutritionValueMult
        profitRatios[1] *= 17
#         
#         print(profitRatios,"profits")
        
        while chose < self.toPlant:
            
            chose += 1
            
            if tempBalance >= Vars.info[1][0] and profitRatios[1] > profitRatios[0] and profitRatios[1] > profitRatios[3] and profitRatios[1] > profitRatios[2]:
                plantOptions[1] += 1
                tempBalance -= Vars.info[1][0]
            
            elif tempBalance >= Vars.info[2][0] and profitRatios[2] > profitRatios[0] and profitRatios[2] > profitRatios[3]:
                plantOptions[2] += 1
                tempBalance -= Vars.info [2][0]
                
            elif tempBalance >= Vars.info[0][0] and profitRatios[0] > profitRatios[3]:
                plantOptions[0] += 1
                tempBalance -= Vars.info [0][0]
                
            elif tempBalance >= Vars.info[3][0]:
                plantOptions[3] += 1
                tempBalance -= Vars.info [3][0]
                
            else:
                return plantOptions
        return plantOptions
    
    def greedyInfo(self):
    
        nutritionValueMult = 0
        
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c].type == "farmland":
                    nutritionValueMult += Vars.nutritionMultipliers[4-self.grid[r][c].nutritionLevel]
        
        nutritionValueMult /= (Vars.NUM_PLOT ** 2)
        plantOptions = self.greedyBestPlant(nutritionValueMult)
        
        return nutritionValueMult, plantOptions
    
    def greedyMove(self):
        
        if self.money > Vars.winCondition and Vars.winner == False:
            self.isWinner = True
            Vars.winner = Vars.farmerNames[self.farmerType] + "Farmer"
        
        if self.queue:
            
            self.sinceLastWait += 1
            if self.waitMod != 0 and self.sinceLastWait % self.waitMod == 0:
                self.sinceLastWait = 0
                self.wait()
            else:
                try:
                    self.queue[0]()
                    
                except TypeError:
                    self.queue[0](*self.args[0])
                    del self.args[0]
                del self.queue[0]
        else:
            
            self.tempx, self.tempy = self.x, self.y
            
            self.available,self.seedInInv,self.toPlant,self.readyForHarvest,self.searchNutrition = self.getInfo()
            self.nutritionValueMult, self.plantOptions = self.greedyInfo()
            
            #print(self.plantOptions)
            
            if self.happiness < 30:
                self.action = "resting"
                self.restFull()
                self.sellAllMove()
                             
            elif any(item.stage == 'seed' for item in self.inv) and self.available > 0:
                self.action = "planting"
                self.plantNext()
                
            elif self.readyForHarvest != 0:
                self.action = "harvesting"
                self.harvestNext()
            
            elif self.money > 0 and self.toPlant > 0:
                self.action = "buying"
                self.buyAllMove()
                                   
            elif any(item.stage == 'fully grown' for item in self.inv) and self.shouldSell():
                self.action = "selling"
                self.sellAllMove()
                
            else:
                self.action = "None; resting"
                self.moveRest()
    
    '''
    effi-specific functions
    '''
    
    def effiBestPlant(self,numNeedNutrition):
        
        chose = 0
        tempBalance = self.money
        tempNeedNutrition = numNeedNutrition
        
        plantOptions = [0,0,0,0]
        profitRatios = [0,0,0,0]
        
        for i in range(4):
            profitRatios[i]= Vars.info[i][1]/Vars.info[i][0]
        
        profitRatios[2] *= 5
        profitRatios[3] *= .1
        
#         print(profitRatios,"profits")
        
        while chose < self.toPlant:
            
            chose += 1
            
            if tempNeedNutrition > 0 and tempBalance >= Vars.info[1][0]:
                plantOptions[1] += 1
                tempBalance -= Vars.info[1][0]
                tempNeedNutrition -= 1
            
            elif tempBalance >= Vars.info[2][0] and profitRatios[2] > profitRatios[0] and profitRatios[2] > profitRatios[3]:
                plantOptions[2] += 1
                tempBalance -= Vars.info [2][0]
                
            elif tempBalance >= Vars.info[0][0] and profitRatios[0] > profitRatios[3]:
                plantOptions[0] += 1
                tempBalance -= Vars.info [0][0]
                
            elif tempBalance >= Vars.info[3][0]:
                plantOptions[3] += 1
                tempBalance -= Vars.info [3][0]
                
            else:
                return plantOptions
        return plantOptions
    
    def effiInfo(self):
    
        numNeedNutrition = 0
        
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c].type == "farmland":
                    try:
                        if self.grid[r][c].nutritionLevel < 3 and self.grid[r][c].layers[0].type != 1:
                            numNeedNutrition += 1
                    except AttributeError:
                        if self.grid[r][c].nutritionLevel < 3:
                            numNeedNutrition += 1
        
        plantOptions = self.effiBestPlant(numNeedNutrition)
        
        return numNeedNutrition, plantOptions
    
    def effiMove(self):
        
        if self.money > Vars.winCondition and Vars.winner == False:
            self.isWinner = True
            Vars.winner = Vars.farmerNames[self.farmerType] + "Farmer"
        
        if self.queue:
            
            self.sinceLastWait += 1
            if self.waitMod != 0 and self.sinceLastWait % self.waitMod == 0:
                self.sinceLastWait = 0
                self.wait()
            else:
                try:
                    self.queue[0]()
                    
                except TypeError:
                    self.queue[0](*self.args[0])
                    del self.args[0]
                del self.queue[0]
        else:
            
            self.tempx, self.tempy = self.x, self.y
            
            self.available,self.seedInInv,self.toPlant,self.readyForHarvest,self.searchNutrition = self.getInfo()
            self.numNeedNutrition, self.plantOptions = self.effiInfo()
            
            #print(self.plantOptions)
            
            if self.happiness < 75:
                self.action = "resting"
                self.restFull()
                self.sellAllMove()
                             
            elif any(item.stage == 'seed' for item in self.inv) and self.available > 0:
                self.action = "planting"
                self.plantNext()
                
            elif self.readyForHarvest != 0:
                self.action = "harvesting"
                self.harvestNext()
            
            elif self.money > 0 and self.toPlant > 0:
                self.action = "buying"
                self.buyAllMove()
                                   
            elif any(item.stage == 'fully grown' for item in self.inv) and self.shouldSell():
                self.action = "selling"
                self.sellAllMove()
            else:
                self.action = "None; resting"
                self.moveRest()

    '''
    eco-specific functions
    '''
    
    def ecoBestPlant(self, numNeedNutrition): # creates a list
        
        chose = 0
        tempBalance = self.money
        tempNeedNutrition = numNeedNutrition
        
        plantOptions = [0,0,0,0]
        profitRatios = [0,0,0,0]
        
        for i in range(4):
            profitRatios[i]= Vars.info[i][1]/Vars.info[i][0]
        
        profitRatios[2] *= 1.2
        profitRatios[3] *= .6    
        
#         print(profitRatios,"profits")
        
        while chose < self.toPlant:
            
            chose += 1
            
            if tempNeedNutrition > 0 and tempBalance >= Vars.info[1][0]:
                plantOptions[1] += 1
                tempBalance -= Vars.info[1][0]
                tempNeedNutrition -= 1
            
            elif tempBalance >= Vars.info[2][0] and profitRatios[2] > profitRatios[0] and profitRatios[2] > profitRatios[3]:
                plantOptions[2] += 1
                tempBalance -= Vars.info [2][0]
                
            elif tempBalance >= Vars.info[0][0] and profitRatios[0] > profitRatios[3]:
                plantOptions[0] += 1
                tempBalance -= Vars.info [0][0]
                
            elif tempBalance >= Vars.info[3][0]:
                plantOptions[3] += 1
                tempBalance -= Vars.info [3][0]
                
            else:
                return plantOptions
        return plantOptions
    
    def ecoInfo(self):
        
        numNeedNutrition = 0
        
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c].type == "farmland":
                    try:
                        if self.grid[r][c].nutritionLevel < 4 and self.grid[r][c].layers[0].type != 1:
                            numNeedNutrition += 1
                    except AttributeError:
                        if self.grid[r][c].nutritionLevel < 4:
                            numNeedNutrition += 1
        
        plantOptions = self.ecoBestPlant(numNeedNutrition)
        
        return numNeedNutrition, plantOptions
    
    def ecoMove(self):
        
        if self.money > Vars.winCondition and Vars.winner == False:
            self.isWinner = True
            Vars.winner = Vars.farmerNames[self.farmerType] + "Farmer"
        
        if self.queue:
            
            self.sinceLastWait += 1
            if self.waitMod !=0 and self.sinceLastWait % self.waitMod == 0:
                self.sinceLastWait = 0
                self.wait()
            else:
                try:
                    self.queue[0]()
                    
                except TypeError:
                    self.queue[0](*self.args[0])
                    del self.args[0]
                del self.queue[0]
        else:
            
            self.tempx, self.tempy = self.x, self.y
            
            self.available,self.seedInInv,self.toPlant,self.readyForHarvest,self.searchNutrition = self.getInfo()
            self.numNeedNutrition, self.plantOptions = self.ecoInfo()
            
            #print(self.plantOptions)
            
            if self.happiness < 50:
                self.action = "resting"
                self.restFull()
                self.sellAllMove()
                
            elif any(item.stage == 'seed' for item in self.inv) and self.available > 0:
                self.action = "planting"
                self.plantNext()
                
            elif self.readyForHarvest != 0:
                self.action = "harvesting"
                self.harvestNext()   
                                   
            elif any(item.stage == 'fully grown' for item in self.inv) and self.shouldSell():
                self.action = "selling"
                self.sellAllMove()
            
            elif self.money > 0 and self.toPlant > 0:
                self.action = "buying"
                self.buyAllMove()
                
            else:
                self.action = "None; resting"
                self.moveRest()
                