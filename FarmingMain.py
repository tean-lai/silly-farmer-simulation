from random import randint

import pygame as game

import FarmerVars as Vars
import Farmer
import Panel  # !!!!!
import Crop
from time import sleep

def setup():
    global clock, screen, panelList, day, ticks  # !!!!
    
    game.init()
    
    screen = game.display.set_mode((
        Vars.SCREEN_WIDTH
        , Vars.SCREEN_HEIGHT
    ))
    # screen = game.display.set_mode((0, 0), game.FULLSCREEN)

    screen.fill((255, 255, 255))

    for i in range(0, Vars.NUM_SQUARES + 1):  # these two for loops draw the lines, creating grids
        game.draw.line(screen, (0, 0, 0), (0, Vars.PLOT_SIZE * i), (Vars.SCREEN_WIDTH, Vars.PLOT_SIZE * i))
    for i in range(0, Vars.NUM_SQUARES + 1):
        game.draw.line(screen, (0, 0, 0), (Vars.PLOT_SIZE * i, 0), (Vars.PLOT_SIZE * i, screen.get_height()))

    game.display.set_caption("Monkey Town")  # MONKYTOWN

    for i, farmerType in enumerate(Vars.farmerList):
        Vars.farmerList[i] = Farmer.Farmer(farmerType, i, screen, 5, 0)

    for i in range(len(Vars.panelList)):  # !!!!!!!!!!
        Vars.panelList[i] = Panel.Panel(Vars.panelList[i])
        
    Vars.panelList[-2].update(screen,Vars.day)

    for farmer in Vars.farmerList:  # this is to set up the store tiles to function properly
        for r in range(len(farmer.grid)):
            for c in range(len(farmer.grid[0])):
                tile = farmer.grid[r][c]
                if tile.type == "store":
                    tile.layers[0] = Crop.Crop(tile.subtype, farmer.farm, tile, r, c)

    clock = game.time.Clock()
    game.display.flip()

    # Vars.farmerList[0].grid[7][0].layers[0] = Crop.Crop(2, 0, 7, 0)


def renderGraphics():  # render graphics in this function so it's not BLAHRASPHASPFHWF all over our ain loop

    # for grid in Vars.farmGrid:  # old pointer
    for farmer in Vars.farmerList:  
        for r in range(len(farmer.grid)):
            for c in range(len(farmer.grid)):  
                farmer.grid[r][c].update(screen)

    for panel in Vars.panelList[:2]: # disregarding last panel since it doesn't need to update
        panel.update(screen, Vars.day)
    # infoPanel.update(screen)
    # statPanel.update(screen)

    game.draw.line(screen, (0, 0, 0), (0, Vars.FARM_WIDTH), (Vars.FARM_WIDTH * 2, Vars.FARM_HEIGHT), 5)
    game.draw.line(screen, (0, 0, 0), (Vars.FARM_HEIGHT, 0), (Vars.FARM_WIDTH, Vars.FARM_HEIGHT * 2), 5)
#     for i in range(0, Vars.NUM_SQUARES + 1):  # these two for loops draw the lines, creating grids
#         game.draw.line(screen, (0, 0, 0), (0, Vars.PLOT_SIZE * i), (Vars.SCREEN_WIDTH, Vars.PLOT_SIZE * i))
#     for i in range(0, Vars.NUM_SQUARES + 1):
#         game.draw.line(screen, (0, 0, 0), (Vars.PLOT_SIZE * i, 0), (Vars.PLOT_SIZE * i, Vars.SCREEN_HEIGHT))


def main():

    setup()
    
    sleep(5)
    running = True
    while running:
        if Vars.winner != False:
            Vars.panelList[-1].update(screen, Vars.day)
            game.display.update((Vars.SCREEN_WIDTH + 200, Vars.SCREEN_HEIGHT, 600, 130))
        
        Vars.tick += 1  # !!!!!!!!
        if Vars.tick == Vars.TICKS_PER_DAY:  # !!!!!!!!!!!!!
            Vars.tick = 0  # !!!!!!!!!!!
            Vars.day += 1  # !!!!!!!!!!!1
            for farmer in Vars.farmerList:
                
                if farmer.happiness > 3:
                    farmer.happiness -= 3
                else:
                    farmer.happiness = 0
                    
            buyDeviations = [0,0,0,0] # for daily price/sell deviations
            sellDeviations = [0,0,0,0]
            for i in range(4):
                if i != 1:
                    buyDeviations[i] = randint(Vars.deviationDaily[i][0] * -1, Vars.deviationDaily[i][0])
                    sellDeviations[i] = randint(Vars.deviationDaily[i][1] * -1, Vars.deviationDaily[i][1])
                else:
                    buyDeviations[i] = randint(Vars.deviationDaily[i][0] * -1, Vars.deviationDaily[i][0])
                    sellDeviations[i] = buyDeviations[i]

            for i in range(len(buyDeviations)):
                if buyDeviations[i] + Vars.info[i][0] >= Vars.baseInfo[i][0] - Vars.deviationMaxes[i][0] and buyDeviations[i] + Vars.info[i][0] <= Vars.baseInfo[i][0] + Vars.deviationMaxes[i][0]:
                    if buyDeviations[i] + Vars.info[i][0] > 0:
                        Vars.info[i][0] += buyDeviations[i]
                    else:
                        Vars.info[i][0] = 1
                    
            for i in range(len(sellDeviations)):
                if sellDeviations[i] + Vars.info[i][1] >= Vars.baseInfo[i][1] - Vars.deviationMaxes[i][1] and sellDeviations[i] + Vars.info[i][1] <= Vars.baseInfo[i][1] + Vars.deviationMaxes[i][1]:
                    if sellDeviations[i] + Vars.info[i][1] > 0:
                        Vars.info[i][1] += sellDeviations[i]
                    else:
                        Vars.info[i][1] = 1
                        
        for event in game.event.get():
            if event.type == game.QUIT:  # Easier Quits
                game.display.quit() 
                game.quit()
                exit()
            
            if event.type == game.KEYDOWN:
                 
                for farmer in Vars.farmerList:  # !!!!!!!
                    
                    if farmer.farmerType == "control":  # !!!!!!!!!1

                        farmer.move(event.key)  # !!!!!!!!!!
                    
        for farmer in Vars.farmerList:
                
            if farmer.farmerType != "control":
                    
                farmer.move()


        renderGraphics()

        game.display.update((0,0,Vars.SCREEN_WIDTH,Vars.SCREEN_HEIGHT))
        clock.tick(Vars.MAX_FPS)

main()