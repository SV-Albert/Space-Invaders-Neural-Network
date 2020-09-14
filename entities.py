import pygame
import os
import sys

player_projectile_speed = 7
enemy_projectile_speed = 6

def loadSprite(name):
    sprite_location = os.path.join(os.sys.path[0], "Assets", name)
    return pygame.image.load(sprite_location).convert()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = loadSprite("player.png")
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))

    def move(self, distance):
        self.rect.x += distance


class PlayerProjectile(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = loadSprite("projectile.png")
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))

    def update(self):
        self.rect.y -= player_projectile_speed

class EnemyProjectile(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = loadSprite("enemy_projectile.png")
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))

    def update(self):
        self.rect.y += enemy_projectile_speed
        if self.rect.y >= 440:
            self.kill()