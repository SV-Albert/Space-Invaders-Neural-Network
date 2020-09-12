import pygame
import os

class Entity:
    def __init__ (self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
    
class LangeEnemy(Entity):
    scoreWorth = 10
    pass

class MediumEnemy(Entity):
    scoreWorth = 20
    pass

class SmallEnemy(Entity):
    scoreWorth = 30
    pass

class Player(Entity):
    spriteLocation = os.path.join(os.sys.path[0], "Assets", "player.png")

    def getSprite(self):
        return pygame.image.load(os.path.join(os.sys.path[0], "Assets", "player.png"))
    pass

class Cover(Entity):
    pass