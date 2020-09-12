import pygame
import os
import numpy as np
from entities import Player

pygame.init()
clock = pygame.time.Clock()
screenWidth = 730
screenHeight = 500
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Space Invaders")
grid = []

def play():
    player = Player(0, 440)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_RIGHT] and player.xPos < screenWidth - player.getSprite().get_rect().size[0]: 
            player.xPos = player.xPos + 5
        elif keyPressed[pygame.K_LEFT] and player.xPos > 0: 
            player.xPos = player.xPos - 5

        screen.fill((0, 0, 0))
        screen.blit(player.getSprite(), (player.xPos, player.yPos))
        pygame.display.flip()
        clock.tick(60)
    
play()