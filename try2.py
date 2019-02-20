###TP2!
###Christopher May
###11/27/17


import copy
import pygame
import random
import os
import time
from prettytable import PrettyTable
from pygameFramework import *

red = (255, 51, 51)  #
green = (0, 215, 21)
lightBlue = (66, 217, 244)
blue = (51, 153, 255)  #
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)
orange = (245, 92, 34)  #
yellow = (18, 230, 169)  #
brick = (211, 70, 52)

blueblue = (30, 154, 253)

NORTH = (-1,0)
SOUTH = (1,0)
EAST  = (0,1)
WEST  = (0,-1)


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(os.path.join("images", image_file)).convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gravity = -2
        self.velocity = 0
        self.jumping = False
        self.jumpOffset = 0
        self.baseHeight = 0

    def movePlayer(self, dx, dy, board, game):
        tempx = self.x
        tempy = self.y
        self.x += dx
        while self.x > len(board[0])-1 or self.x < 0:
            self.x -= dx

        self.y += dy
        while self.y > len(board)-1 or self.y <= 0:
            self.y -= dy

        print(self.baseHeight)
        print(game.tileHeight + game.offset)

        board[tempy][tempx] = 2
        for block in game.blocks:
            if block.y == tempy and block.x == tempx:
                board[tempy][tempx] = 3

        if (board[self.y][self.x] == 1 and board[tempy][tempx] != 3) and \
                self.baseHeight + self.jumpOffset < game.tileHeight +game.offset:
            self.y = tempy
            self.x = tempx

    def jump(self, board):
        if self.jumping == False:
            self.jumping = True
            self.velocity = 25

    def update(self,game):
        if self.jumping:
            self.jumpOffset+=self.velocity
            self.velocity+=self.gravity
            if self.jumpOffset <= 0:
                self.jumpOffset = 0
                self.jumping = False
                self.velocity = 0
                for block in game.blocks:
                    if block.y == self.y and block.x == self.x:
                        #game.board[self.y][self.x] = 3
                        self.baseHeight = game.tileHeight + block.blockOffset
        # else:
        #     if game.board[self.y][self.x] == 3:
        #         self.baseHeight = 30
        #         if self.y <= 5:
        #             print("set to 1")
        #             #game.board[self.y][self.x] = 1
        #         else:
        #             game.mode = "game over"
        #         for block in game.blocks:
        #             if block.y == self.y and block.x == self.x:
        #                 return
                #game.board[self.y][self.x] = 2


    def drawPlayer(self,screen,game):
        pt = Point((self.x-1) * game.tileWidth-game.offset,
                   (self.y -1) * game.tileHeight-game.offset)
        self.placeTile(game, screen, 1, pt, white)
        self.placeLBase(game, screen, 1, pt, white)
        self.placeRBase(game, screen, 2, pt, white)
        self.placeTile(game, screen, 1, pt, black, 2)
        self.placeLBase(game, screen, 1, pt, black, 2)
        self.placeRBase(game, screen, 2, pt, black, 2)

    def placeTile(self,game,screen, tile, pt, color=red, width=0):
        pointsList = [runGame.twoDToIso(game, pt.x, pt.y),
                      runGame.twoDToIso(game,pt.x + game.tileWidth, pt.y),
                      runGame.twoDToIso(game,pt.x + game.tileWidth,
                                        pt.y + game.tileHeight),
                      runGame.twoDToIso(game,pt.x, pt.y + game.tileHeight)]
        for i in range(len(pointsList)):
            pointsList[i] = (pointsList[i][0] + game.width / 2,
                             pointsList[i][1] + game.height / 3-self.jumpOffset-self.baseHeight)
        if (tile == 7 or tile == 3 or tile ==4) and color != black:
            color = green
        elif tile == 0 and color != black:
            color = blue
        pygame.draw.polygon(screen, color, pointsList, width)
        # pygame.draw.polygon(screen, color,
        #                    [(pt.x, pt.y), (pt.x + game.tileWidth, pt.y),
        #                     (pt.x + game.tileWidth, pt.y + game.tileHeight),
        #                     (pt.x, pt.y + game.tileHeight)], width)

    def placeLBase(self,game, screen, tile, pt, color=red, width=0):
        if tile == 1 or tile == 5 or tile == 6:
            pointsList = [runGame.twoDToIso(game, pt.x, pt.y + game.tileHeight),
                          runGame.twoDToIso(game, pt.x + game.tileWidth+game.offset,
                                            pt.y + game.tileHeight * 2+game.offset),
                          runGame.twoDToIso(game, pt.x + game.tileWidth * 2+game.offset,
                                            pt.y + game.tileHeight * 2+game.offset),
                          runGame.twoDToIso(game, pt.x + game.tileWidth,
                                            pt.y + game.tileHeight)]
            for i in range(len(pointsList)):
                pointsList[i] = (pointsList[i][0] + game.width /2,
                                 pointsList[i][1] + game.height /3-self.jumpOffset-self.baseHeight)

            pygame.draw.polygon(screen, color, pointsList, width)

    def placeRBase(self,game, screen, tile, pt, color=red, width=0):
        if tile == 2 or tile == 5 or tile == 4:
            pointsList = [runGame.twoDToIso(game, pt.x + game.tileWidth, pt.y + game.tileHeight),
                          runGame.twoDToIso(game, pt.x + game.tileWidth * 2+game.offset,
                                            pt.y + game.tileHeight * 2+game.offset),
                          runGame.twoDToIso(game, pt.x + game.tileWidth * 2+game.offset,
                                            pt.y + game.tileHeight+game.offset),
                          runGame.twoDToIso(game, pt.x + game.tileWidth,
                                            pt.y)]
            for i in range(len(pointsList)):
                pointsList[i] = (pointsList[i][0] + game.width / 2,
                                 pointsList[i][1] + game.height / 3-self.jumpOffset-self.baseHeight)
            if tile == 4 and color != black:
                color = green
            pygame.draw.polygon(screen, color, pointsList, width)



class Block(object):
    def __init__(self, x, y=0, height=50):
        self.x = x
        self.y = y
        self.height = height
        self.blockOffset = random.randint(0,2)
        if self.blockOffset == 0:
            self.blockOffset = -20
            self.color = orange
        elif self.blockOffset == 1:
            self.blockOffset = 10
            self.color = red
        elif self.blockOffset == 2:
            self.blockOffset = 40
            self.color = yellow

        #####STORE

    def moveBlockDown(self):
        self.y += 1
        if self.y > 5:
            self.y -= 1
            return False
        return True

    def __eq__(self, other):
        return isinstance(other, Block) and (
        self.x == other.x and self.y == other.y and self.height == other.height)

    def __hash__(self):
        return hash((self.x, self.y, self.height))

    def __repr__(self):
        return "Block(%s,%s)" % (self.x,self.y)

    def drawBlock(self,screen, pt, game):
        pt = Point((pt.x-1) * game.tileWidth - self.blockOffset,
                   (pt.y-1) * game.tileHeight - self.blockOffset)
        Block.placeTile(self, screen, game, 1, pt, self.color)
        Block.placeLBase(self, screen, game, 1, pt, self.color)
        Block.placeRBase(self, screen, game, 2, pt, self.color)
        Block.placeTile(self, screen, game, 1, pt, black, 2)
        Block.placeLBase(self, screen, game, 1, pt, black, 2)
        Block.placeRBase(self, screen, game, 2, pt, black, 2)

    def placeTile(self, screen, game, tile, pt, color=red, width=0):
        pointsList = [runGame.twoDToIso(game, pt.x, pt.y),
                      runGame.twoDToIso(game,pt.x + game.tileWidth, pt.y),
                      runGame.twoDToIso(game,pt.x + game.tileWidth,
                                        pt.y + game.tileHeight),
                      runGame.twoDToIso(game,pt.x, pt.y + game.tileHeight)]
        for i in range(len(pointsList)):
            pointsList[i] = (pointsList[i][0] + game.width / 2,
                             pointsList[i][1] + game.height / 3)
        if (tile == 7 or tile == 3 or tile ==4) and color != black:
            color = green
        elif tile == 0 and color != black:
            color = blue
        pygame.draw.polygon(screen, color, pointsList, width)

    def placeLBase(self, screen, game, tile, pt, color=red, width=0):
        if tile == 1 or tile == 5 or tile == 6:
            pointsList = [runGame.twoDToIso(game, pt.x, pt.y + game.tileHeight),
                          runGame.twoDToIso(game, pt.x + game.tileWidth+self.blockOffset,
                                            pt.y + game.tileHeight * 2+self.blockOffset),
                          runGame.twoDToIso(game, pt.x + game.tileWidth * 2+self.blockOffset,
                                            pt.y + game.tileHeight * 2+self.blockOffset),
                          runGame.twoDToIso(game, pt.x + game.tileWidth,
                                            pt.y + game.tileHeight)]
            for i in range(len(pointsList)):
                pointsList[i] = (pointsList[i][0] + game.width / 2,
                                 pointsList[i][1] + game.height /3)

            pygame.draw.polygon(screen, color, pointsList, width)

    def placeRBase(self, screen, game, tile, pt, color=red, width=0):
        if tile == 2 or tile == 5 or tile == 4:
            pointsList = [runGame.twoDToIso(game, pt.x + game.tileWidth, pt.y + game.tileHeight),
                          runGame.twoDToIso(game, pt.x + game.tileWidth * 2+self.blockOffset,
                                            pt.y + game.tileHeight * 2+self.blockOffset),
                          runGame.twoDToIso(game, pt.x + game.tileWidth * 2+self.blockOffset,
                                            pt.y + game.tileHeight+self.blockOffset),
                          runGame.twoDToIso(game, pt.x + game.tileWidth,
                                            pt.y)]
            for i in range(len(pointsList)):
                pointsList[i] = (pointsList[i][0] + game.width / 2,
                                 pointsList[i][1] + game.height / 3)
            if tile == 4 and color != black:
                color = green
            pygame.draw.polygon(screen, color, pointsList, width)

class runGame(pygameGame):
    def init(self):
        pass

    def mousePressed(self, x, y):
        if self.mode == "main menu":
            if x > self.width / 5 and x < self.width /5 + 150:
                if y > (self.height - self.height / 3) and \
                                y < self.height - self.height / 3 + 75:
                    #if self.blocks == set():
                        #self.blocks.add(Block(2,-1))
                    self.mode = "difficulty"
                    #self.blocks = set()
                    self.time = 0
            if x > self.width / 2 + 45 and x < self.width / 2+45+150:
                if y > self.height - self.height / 3 and \
                                y < self.height - self.height / 3 + 75:
                    pygame.quit()
        elif self.mode == "difficulty":
            if x > self.width / 2-70 and x < self.width / 2-70 + 142:
                if y > self.height / 2 - 57 and y < self.height / 2 - 57 + 60:
                    self.timerDelay = 1000
                    self.mode = "playing"
                if y > self.height / 2 + 43 and y < self.height / 2 + 43 + 60:
                    self.timerDelay = 600
                    self.mode = "playing"
                if y > self.height / 2 + 142 and y < self.height / 2 + 142 + 60:
                    self.timerDelay = 300
                    self.mode = "playing"

    def timerFired(self, time):
        if self.mode == "playing" and not self.paused:
            self.time += time
            if self.blocks != set():
                self.score += 1

            runGame.updateBoard(self)
            if self.time > self.timerDelay:
                runGame.addLegalBlock(self)

                blocksToKeep = set()
                movePlayerDown = False
                for block in self.blocks:
                    if block.moveBlockDown() == True:
                        #move the player as well if player is on top of this block
                        if self.player.baseHeight + self.player.jumpOffset <= self.tileHeight+block.blockOffset:
                            if self.player.x == block.x and self.player.y == block.y:
                                movePlayerDown = True
                            # else:
                            #     if block.y == self.player.y -1 and block.x == self.player.x:
                            #
                            #         self.player.y += 1
                            #         if self.player.y > 5:
                            #             self.mode = "game over"
                        blocksToKeep.add(block)
                if movePlayerDown:
                    self.player.y += 1
                    if self.player.y > 5:
                        self.mode = "game over"
                        self.highScore.append(self.score)
                self.blocks = blocksToKeep
                self.time = 0

    def keyPressed(self, keyCode, modifier):
        if self.mode == "playing":
            if not self.player.jumping:
                if keyCode == pygame.K_LEFT:
                    Player.movePlayer(self.player,-1, 0, self.board, self)
                    print(self.player.x, self.player.y)
                elif keyCode == pygame.K_RIGHT:
                    Player.movePlayer(self.player,1, 0, self.board, self)
                    print(self.player.x, self.player.y)
                elif keyCode == pygame.K_UP:
                    Player.movePlayer(self.player,0, -1, self.board, self)
                    print(self.player.x, self.player.y)
                elif keyCode == pygame.K_DOWN:
                    Player.movePlayer(self.player,0, 1, self.board, self)
                    print(self.player.x, self.player.y)
                elif keyCode == pygame.K_SPACE:
                    Player.jump(self.player, self.board)
            if keyCode == pygame.K_p:
                if not self.paused:
                    self.paused = True
                else:
                    self.paused = False
        if keyCode == pygame.K_m:
            runGame.resetForNewGame(self)
        elif keyCode == pygame.K_ESCAPE:
            pygame.quit()

    def resetForNewGame(self):
        self.time = 0
        self.mode = "main menu"
        self.player = Player(3, 5)
        self.board = self.board = [[None] * self.cols for i in range(self.rows)]
        self.blocks = set()
        self.score = 0

    def __init__(self, width=600, height=600, fps=30, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.player = Player(3,5)
        self.time = 0
        self.mode = "main menu"
        self.timerDelay = 500
        self.paused = False

        self.rows = 6
        self.cols = 6
        self.board = [[None] * self.cols for i in range(self.rows)]
        self.tileWidth = 50 #has to be equal
        self.tileHeight = 50 #has to be equal
        self.offset = -20
        self.score = 0
        self.highScore = []

        self.levelData = [[3,7,7,7,7,4],
                          [0,0,0,0,0,0],
                          [0,0,0,0,0,0],
                          [0,0,0,0,0,0],
                          [0,0,0,0,0,0],
                          [0,0,0,0,0,0]]

        self.blocks = set()
        pygame.init()


    def drawMenu(self, screen):
        screen.fill(white)
        screen.blit(self.menuBackground.image, self.menuBackground.rect)
        runGame.message_display(self, "Welcome to Tile Run!", screen, 40,
                                (self.width / 2, self.height / 3))
        runGame.message_display(self, "Made by CJ May", screen, 40,
                                (self.width / 2, self.height / 2))
        pygame.draw.rect(screen, black, (
            self.width / 5, self.height - self.height / 3, 150,
            75), 3)
        pygame.draw.rect(screen, black, (
            self.width / 2+45, self.height - self.height / 3, 150,
            75), 3)
        runGame.message_display(self, "Play", screen, 40,(
        self.width / 5 + 75, self.height - self.height / 3 + 40))
        runGame.message_display(self, "Quit", screen, 40, (
            self.width / 5 + 312, self.height - self.height / 3 + 40))

    def text_objects(self, text, font):
        textSurface = font.render(text, True, white)
        return textSurface, textSurface.get_rect()

    def message_display(self, text, screen, size, location):
        largeText = pygame.font.Font('freesansbold.ttf', size)
        TextSurf, TextRect = runGame.text_objects(self, text, largeText)
        TextRect.center = location
        screen.blit(TextSurf, TextRect)

    def drawInstructions(self, screen):
        runGame.message_display(self, "Use the arrow keys to move!", screen, 30,
                                (self.width / 2, 75))
        runGame.message_display(self, "Press 'm' for menu", screen, 20, (110, self.height-30))
        runGame.message_display(self, "Score: %s" % (self.score), screen, 24,
                                (self.width /2, 130))

    def drawGrid(self, screen):
        for i in range(self.rows):
            for j in range(self.cols):
                x = j * self.tileWidth
                y = i * self.tileHeight
                tileType = self.levelData[i][j]
                runGame.placeLBase(self,screen,tileType,Point(x,y), blue, 0)
                runGame.placeLBase(self,screen,tileType,Point(x,y), black, 2)
                runGame.placeRBase(self,screen,tileType,Point(x,y),blue ,0)
                runGame.placeRBase(self,screen,tileType,Point(x,y),black, 2)
                runGame.placeTile(self, screen, tileType, Point(x,y), blue)
                runGame.placeTile(self, screen, tileType, Point(x, y), black, 2)

    def placeTile(self, screen, tile, pt, color=blue, width=0):
        pointsList = [runGame.twoDToIso(self, pt.x, pt.y),
                      runGame.twoDToIso(self,pt.x + self.tileWidth, pt.y),
                      runGame.twoDToIso(self,pt.x + self.tileWidth,
                                        pt.y + self.tileHeight),
                      runGame.twoDToIso(self,pt.x, pt.y + self.tileHeight)]
        for i in range(len(pointsList)):
            pointsList[i] = (pointsList[i][0] + self.width / 2,
                             pointsList[i][1] + self.height / 3)
        if (tile == 7 or tile == 3 or tile ==4) and color != black:
            color = blue
        elif tile == 0 and color != black:
            color = blue
        pygame.draw.polygon(screen, color, pointsList, width)
        # pygame.draw.polygon(screen, color,
        #                    [(pt.x, pt.y), (pt.x + self.tileWidth, pt.y),
        #                     (pt.x + self.tileWidth, pt.y + self.tileHeight),
        #                     (pt.x, pt.y + self.tileHeight)], width)

    def placeLBase(self, screen, tile, pt, color=brick, width=0):
        if tile == 1 or tile == 0 or tile == 5 or tile == 6:
            pointsList = [runGame.twoDToIso(self, pt.x, pt.y + self.tileHeight),
                          runGame.twoDToIso(self, pt.x + self.tileWidth+self.offset,
                                            pt.y + self.tileHeight * 2+self.offset),
                          runGame.twoDToIso(self, pt.x + self.tileWidth * 2+self.offset,
                                            pt.y + self.tileHeight * 2+self.offset),
                          runGame.twoDToIso(self, pt.x + self.tileWidth,
                                            pt.y + self.tileHeight)]
            for i in range(len(pointsList)):
                pointsList[i] = (pointsList[i][0] + self.width / 2,
                                 pointsList[i][1] + self.height /3)

            pygame.draw.polygon(screen, color, pointsList, width)

    def placeRBase(self, screen, tile, pt, color=brick, width=0):
        if tile == 2 or tile == 5 or tile == 4 or tile == 0:
            pointsList = [runGame.twoDToIso(self, pt.x + self.tileWidth, pt.y + self.tileHeight),
                          runGame.twoDToIso(self, pt.x + self.tileWidth * 2+self.offset,
                                            pt.y + self.tileHeight * 2+self.offset),
                          runGame.twoDToIso(self, pt.x + self.tileWidth * 2+self.offset,
                                            pt.y + self.tileHeight+self.offset),
                          runGame.twoDToIso(self, pt.x + self.tileWidth,
                                            pt.y)]
            for i in range(len(pointsList)):
                pointsList[i] = (pointsList[i][0] + self.width / 2,
                                 pointsList[i][1] + self.height / 3)
            if tile == 4 and color != black:
                color = blue
            pygame.draw.polygon(screen, color, pointsList, width)

    def twoDToIso(self, x, y):
        return ((x - y, (x + y) / 2))

    def isoTo2d(self, x, y):
        return (((2 * y + x) / 2, (2 * y - x) / 2))

    def drawEntities(self,screen):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[col][row] == 2:
                    self.player.drawPlayer(screen,game)
                elif self.board[col][row] == 3:
                    for block in self.blocks:
                        if block.x == row and block.y == col:
                            block.drawBlock(screen, Point(row, col), game)
                            self.player.drawPlayer(screen, game) ###THAT WE PASS HIGHER HEIGHT
                else:
                    for block in self.blocks:
                        #print("jdksfl", block.x,block.y)
                        if block.x == row and block.y == col:
                            block.drawBlock(screen,Point(row, col), game)


    def addLegalBlock(self):
        ranInt = random.randint(0,5)
        for num in random.sample(range(6), ranInt):
            b = Block(num, -1)

            newBoard = copy.deepcopy(self.board)
            newBoard[b.y+1][b.x] = 1
            newBoard[self.player.y][self.player.x] = 2
            for block in self.blocks:
                if block.y == self.player.y and block.x == self.player.x:
                    newBoard[self.player.y][self.player.x] = 3

            # print("supposed new board")
            # for row in newBoard:
            #     for val in row:
            #         if val == None:
            #             print("None", end="\t")
            #         else:
            #             print("{:4}".format(val), end="\t")
            #     print("")
            #     # print("BLOCK:", block.x,block.y)
            #     # if block.x == self.player.x and block.y == self.player.y+1:
            #     # Player.movePlayer(self.player, 0, +1, self.board)
            # print()
            # print("supposed old board")
            # for row in self.board:
            #     for val in row:
            #         if val == None:
            #             print("None", end="\t")
            #         else:
            #             print("{:4}".format(val), end="\t")
            #     print("")
            #     # print("BLOCK:", block.x,block.y)
            #     # if block.x == self.player.x and block.y == self.player.y+1:
            #     # Player.movePlayer(self.player, 0, +1, self.board)
            #
            # print(self.blocks)
            #
            # print("\n\n")

            if not runGame.solveMaze(self, newBoard):
                # print(self.board)
                # print("Got here")
                pass
            else:
                self.board = copy.deepcopy(newBoard)
                self.blocks.add(b)
            if not runGame.solveMaze(self, self.board):
                if newBoard[self.player.y][self.player.x] != 3 and self.player.y > 5:
                    print("fail")
                    self.mode = "game over"

                    self.highScore.append(self.score)

            newBoard = None

    def isValid(maze, row, col): #From 15-112 Backtracking notes
        ###SHOULD ONLY CHECK POSITION ON BOARD
        rows, cols = len(maze), len(maze[0])
        if not (0 <= row < rows and 0 <= col < cols): return False
        return maze[row][col] == None

    def solveMaze(self, maze): #Taken from 15-112 backtracking notes (modified)
        rows, cols = len(maze), len(maze[0])
        visited = set()
        targetRow, targetCol = 0, 0

        def solve(row, col):
            # base cases
            if (row, col) in visited: return False
            visited.add((row, col))
            if row == targetRow:
                return True
            # recursive case
            for drow, dcol in [NORTH, SOUTH, EAST, WEST]:
                if runGame.isValid(maze, row+drow, col+dcol):
                    if solve(row + drow, col + dcol): return True
            visited.remove((row, col))
            return False
        return True if solve(self.player.y,
                                    self.player.x) else False

    def updateBoard(self):
        tempBoard = [[None] * self.cols for i in range(self.rows)]
        tempBoard[self.player.y][self.player.x] = 2
        movePlayerDown = False
        tempHeight = 0
        for block in self.blocks:
            if block.x == self.player.x and block.y == self.player.y:
                tempBoard[self.player.y][self.player.x] = 3

                tempHeight = self.tileHeight + block.blockOffset
                if self.tileHeight + block.blockOffset >= tempHeight + self.player.jumpOffset:
                    if not self.player.jumping:
                        movePlayerDown = True
            else:
                tempBoard[block.y][block.x] = 1
        # if movePlayerDown:
        #     self.player.y += 1

        self.player.baseHeight = tempHeight

        self.board = copy.deepcopy(tempBoard)
        self.player.update(self)
        # for row in self.board:
        #     for val in row:
        #         if val == None:
        #             print("None", end="\t")
        #         else:
        #             print("{:4}".format(val), end="\t")
        #     print("")
        # print()

    def drawDiff(self, screen):
        screen.fill(white)
        screen.blit(self.menuBackground.image, self.menuBackground.rect)
        pygame.draw.rect(screen, black, (
            self.width / 2-70, self.height / 2 - 57, 142,
            60), 3)
        pygame.draw.rect(screen, black, (
            self.width / 2 - 70, self.height / 2 + 43, 142,
            60), 3)
        pygame.draw.rect(screen, black, (
            self.width / 2 - 70, self.height / 2 + 142, 142,
            60), 3)
        #runGame.message_display(self, "Play", screen, 40, (
            #self.width / 5 + 75, self.height - self.height / 3 + 40))

        runGame.message_display(self, "Press 'm' for menu", screen, 20,
                                (110, self.height - 30))
        runGame.message_display(self, "Choose difficulty", screen, 40,
                                (self.width / 2, self.height /4))
        runGame.message_display(self, "Easy", screen, 30,
                                (self.width/2, self.height /2 - 25))
        runGame.message_display(self, "Medium", screen, 30,
                                (self.width / 2, self.height / 2+75))
        runGame.message_display(self, "Hard", screen, 30,
                                (self.width / 2, self.height / 2+175))

    def drawEnd(self, screen):
        screen.fill(white)
        screen.blit(self.menuBackground.image, self.menuBackground.rect)
        runGame.message_display(self, "Game over!", screen, 40,
                                (self.width / 2, self.height / 2-150))
        runGame.message_display(self,
                                "High Scores", screen, 20,
                                (self.width / 2, self.height / 2 - 100))
        self.highScore.sort(reverse = True)
        for i in range(len(self.highScore)):
            runGame.message_display(self, "%s. %s" % (str(i+1), self.highScore[i]), screen, 20,
                                (self.width / 2, self.height / 2-70+i*30))
        runGame.message_display(self, "Press 'm' to play again!", screen, 20,
                                (130, self.height - 30))

    def redrawAll(self, screen):
        if self.mode == "main menu":
            runGame.drawMenu(self,screen)

        if self.mode == "difficulty":
            runGame.drawDiff(self, screen)

        if self.mode == "playing":
            screen.fill(white)
            screen.blit(self.menuBackground.image, self.menuBackground.rect)
            runGame.drawInstructions(self,screen)
            runGame.drawGrid(self, screen)
            runGame.drawEntities(self, screen)

        if self.mode == "game over":
            runGame.drawEnd(self, screen)

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        self.menuBackground = Background('cj pic.png', [0, 0])
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                              event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                              event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()


game = runGame(650,650,25,"Run v4!")
game.run()