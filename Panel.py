import pygame as game

import FarmerVars as Vars


class Panel:

    def __init__(self, lis):
        self.color, self.x, self.y, self.width, self.height, self.configuration = lis

        self.panel = game.Rect(self.x, self.y, self.width, self.height)
        self.lines_printed = 0  # will help make print function work

    def update(self, screen, day):
        self.lines_printed = 0
        self.draw(screen, day)

    def draw(self, screen, day):
        game.draw.rect(screen, self.color, self.panel)

        if self.configuration == "info":
            self.print(screen, "Crop Info: [buy price/sell price/days to grow/nutrition/fail rate]")
            self.print(screen, "")
            for i in range(len(Vars.info)):
                string = ""
                string += Vars.plantTypes[i]
                string += " Plant: ["
                string += "/".join([str(j) for j in Vars.info[i]])
                string += "]"
                self.print(screen, string)

        elif self.configuration == "stat":
            self.print(screen, "Day: " + str(day))
            self.print(screen, "")

            for i, farmer in enumerate(Vars.farmerList):
                self.print(screen, "")
                self.print(screen, str(Vars.farmerNames[Vars.farmerList[i].farmerType]) + "Farmer")
                self.print(screen, "Money: " + str(farmer.money))
                self.print(screen, "Happiness: " + str(farmer.happiness))
                self.print(screen, "Action: " + str(farmer.action))

        elif self.configuration == "instructions":
            self.print(screen, "This is a simulation of farmers and farming")
            self.print(screen, "")
            self.print(screen, "The program finds which farmer algorithm is the best")
            self.print(screen, "Is it the eco farmer, the one who keeps dirt nutritional?")
            self.print(screen, "Is it the greedy farmer, the one who goes for the most profits?")
            self.print(screen, "Is it the effiency farmer, who is picky with his sell prices?")
            self.print(screen, "Is it the monkey farmer, who relies on chance and randomness?")
            self.print(screen, "")
            self.print(screen, "Different plants have different rates of failure. Poor")
            self.print(screen, "nutrition levels in the soil will raise the chances of failure.")
            self.print(screen, "Brighter tiles of soil have less nutrients.")
            self.print(screen, "")
            self.print(screen, "Plant prices also fluctuate daily, sometimes plants can")
            self.print(screen, "be cheap or expensive, life is RNG sometimes, you know?")
            self.print(screen, "")
            self.print(screen, "The goal is $10,000, the first one to reach that wins!")
        
        elif self.configuration == "winner":
            if Vars.winner != False:
                self.print(screen, "Winner is: " + str(Vars.winner))

    def print(self, screen, text):  # works like a print function but for the panel instead of a console
        font = game.font.SysFont("Comic Sans MS", 20)  # this font sucks
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (self.x, self.y + 20 * self.lines_printed))
        self.lines_printed += 1