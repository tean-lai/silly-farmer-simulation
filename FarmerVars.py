import pygame as game
'''
Here to provide MonkeyTown's GLOBAL variables
'''

nutritionThreshold = [80, 60, 40, 20, 0]
happinessThreshold = [80, 60, 40, 20, 0]

soilColors = [(107, 40, 9), (161, 62, 16), (183, 82, 36), (196, 109, 68), (237, 156, 119)]

nutritionMultipliers = [1.5, 1, .7, .5, .3]
happinessTimers = [0, 6, 5, 3, 2]

farmerNames = {
    "eco": "Eco-Friendly ",
    "effi": "Efficiency ",
    "monkey": "Monkey ",
    "greedy": "Greedy "
    }

class Tile:
    def __init__(self, farmNum, row, col, type="nothing", subtype="nothing"):
        self.farmNum = farmNum
        self.xShift = 0
        self.yShift = 0
        if self.farmNum == 1 or self.farmNum == 3:  # shifted so the tiles will draw on separate
            self.xShift += PLOT_SIZE * NUM_SQUARES  # areas on the screen and not all on top
        if self.farmNum == 2 or self.farmNum == 3:  # of each other
            self.yShift += PLOT_SIZE * NUM_SQUARES
        
        self.type = type
        self.subtype = subtype  # gives each store an id which determines what plants can be bought from that store
        if self.type == "nothing":
            self.color = (255, 255, 255)
        elif self.type == "barn":
            self.color = (255, 0, 0)
        elif self.type == "farmland":
            self.color = (113, 87, 70)
            self.nutrition = 100
            self.multiplier = .6
            self.nutritionLevel = 4
            
        elif self.type == "store":
            self.color = (0, 255, 0)

        self.size = PLOT_SIZE
        self.x = col * self.size + self.xShift
        self.y = row * self.size + self.yShift

        self.layers = [0 for __ in range(2)]  # draws things in order based on layers


    def update(self, screen):  # !!!!!!!!!!1
        
        if self.type == "farmland":
            for i,threshold in enumerate(nutritionThreshold):
                if self.nutrition > threshold:
                    self.color = soilColors[i]
                    self.multiplier = nutritionMultipliers[i]
                    self.nutritionLevel = 4-i
                    break
                
        self.draw(screen)

        for thing in self.layers:
            if thing:
                thing.update(screen)

    def draw(self, screen):  # !!!!!!!!1
        game.draw.rect(
            screen,
            self.color,
            game.Rect(
                self.x,
                self.y,
                self.size,
                self.size
            )
        )


'''
INITIATE MONKEYTOWN
'''

MAX_FPS = 30
PLOT_SIZE = 32
NUM_SQUARES = 8  # must be a minimal of of 6 squares and 3 more than num_plot !!!!!
NUM_PLOT = 6  # must be less than NUMS_SQUARES
STARTING_MONEY = 100
NUM_OF_FARMS = 4  # only divisible by 2
FARM_WIDTH = FARM_HEIGHT = NUM_SQUARES * PLOT_SIZE  # !!!!!!!!!!!
SCREEN_WIDTH = FARM_WIDTH * 2  # !!!!!!!!1111
SCREEN_HEIGHT = FARM_HEIGHT * 2  # !!!!!!!!!!!!
TICKS_PER_DAY = 20
day = 0
tick = 0


'''
FarmerVars
'''

farmerList = ["eco", "effi", "monkey", "greedy"]
restAmt = 3
winner = False
winCondition = 10000

'''
Keeping track of the plots and stuff
'''

farmGrid = [[[0 for i in range(NUM_SQUARES)] for j in range(NUM_SQUARES)] for k in range(NUM_OF_FARMS)]  # the grid map of our beautiful farm  
for farmNum, grid in enumerate(farmGrid):  # iterates through the multiple grids !!!!!!!!!

    for r in range(1):  # !!!!!!!!!!!!!!
        for c in range(3):  # !!!!!!!!!!!!!
            grid[r][c] = Tile(farmNum, r, c, type="barn")  # !!!!!!!!!11111

    for r in range(NUM_SQUARES - NUM_PLOT, NUM_SQUARES):
        for c in range(NUM_PLOT):
            grid[r][c] = Tile(farmNum, r, c, type="farmland")  # !!!!!!!!!!

    i = 0  # !!!!!!!!!!!!
    for r in range(1, len(grid), 2):  # !!!!!!!!
        grid[r][NUM_SQUARES - 1] = Tile(farmNum, r, NUM_SQUARES - 1, type="store", subtype=i)  # !!!!!!!!!!!!
        i += 1  # !!!!!!!!!!1

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 0:
                grid[r][c] = Tile(farmNum, r, c)


'''
Font/Text
'''

game.font.init()


def makeText(text, font, color):  # Nifty function that just easily creates a text box and also returns its rectangle
    textSur = font.render(text, True, color)
    return textSur, textSur.get_rect()  # Ex: statText,statRect = makeText(), change position of statRect, game.blit(statText,statRect)


'''
Colors
'''

BROWN = (113, 87, 70)  # this is my dirt color
GREY = (200, 200, 200)

'''
Panels
'''

panelList = [  # !!!!!! contains info for the panels
    # leftCorner's x value,
    # leftCorner's y value,
    # width,
    # height,
    # configuration
    [GREY, 0, SCREEN_HEIGHT, SCREEN_WIDTH + 200, 130, "info"],
    [GREY, SCREEN_WIDTH, 0, 200, SCREEN_HEIGHT, "stat"],
    [BROWN, SCREEN_HEIGHT + 200, 0, 600, SCREEN_HEIGHT, "instructions"],
    [BROWN, SCREEN_WIDTH + 200, SCREEN_HEIGHT, 600, 130, "winner"]
    # [(0, 127, 127), SCREEN_HEIGHT + 200, SCREEN_HEIGHT, 600, 200, "???"]
]

# the following lines of code is to calculate the screen width and height after adding in panels !!!!!!!
for panelInfo in panelList:  # !!!!!!!!!!!!!!!!!!
    testWidth = panelInfo[1] + panelInfo[3]
    testHeight = panelInfo[2] + panelInfo[4]
    if testWidth > SCREEN_WIDTH:
        SCREEN_WIDTH = testWidth
    if testHeight > SCREEN_HEIGHT:
        SCREEN_HEIGHT = testHeight

'''
Plants [Buy Price, Sell Price, Days to Grow, Nutrition Value, Chance 2 Fail]
'''

stages = ["seed", "fully grown"]
info = [  
    [50, 300, 10, -20, 20],
    [5, 5, 8, 30, 0],
    [500, 10000, 10, -100, 30],
    [1, 20, 2, -20, 50]
]

deviationMaxes = [[10, 10], [5, 5], [250, 2000], [0, 10]]
deviationDaily = [[2, 3], [1], [50, 250], [0, 5]]
baseInfo = [  
    [50, 300, 10, -20, 20],
    [5, 5 , 8, 30, 0],
    [500, 10000, 10, -100, 30],
    [1, 20, 2, -20, 50]
]

plantTypes = [
    "Normal",
    "Nutrient",
    "Royal",
    "Basic"
]