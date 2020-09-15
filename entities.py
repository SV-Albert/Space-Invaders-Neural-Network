import pygame
import os
import sys

player_projectile_speed = 10
enemy_projectile_speed = 7


def loadSprite(name):
    sprite_location = os.path.join(os.sys.path[0], "Assets", name)
    return pygame.image.load(sprite_location).convert()


square_barrier = [loadSprite("square100.png"), loadSprite("square75.png"), loadSprite("square50.png"), loadSprite("square25.png")]
top_right_barrier = [loadSprite("topright100.png"), loadSprite("topright75.png"), loadSprite("topright50.png"), loadSprite("topright25.png")]
top_left_barrier = [loadSprite("topleft100.png"), loadSprite("topleft75.png"), loadSprite("topleft50.png"), loadSprite("topleft25.png")]
bottom_left_barrier = [loadSprite("bottomleft100.png"), loadSprite("bottomleft75.png"), loadSprite("bottomleft50.png"), loadSprite("bottomleft25.png")]
bottom_right_barrier = [loadSprite("bottomright100.png"), loadSprite("bottomright75.png"), loadSprite("bottomright50.png"), loadSprite("bottomright25.png")]
barriers = [square_barrier, top_right_barrier, top_left_barrier, bottom_left_barrier, bottom_right_barrier]



class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = loadSprite("player.png")
        self.rect = self.image.get_rect(center=(pos[0], pos[1]))

    def move(self, distance):
        self.rect.x += distance

    def destroy(self):
        self.image = loadSprite("player_dead.png")


class PlayerProjectile(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = loadSprite("projectile.png")
        self.rect = self.image.get_rect(center=(pos[0], pos[1]))

    def update(self):
        self.rect.y -= player_projectile_speed

class EnemyProjectile(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = loadSprite("enemy_projectile.png")
        self.rect = self.image.get_rect(center=(pos[0], pos[1]))

    def update(self):
        self.rect.y += enemy_projectile_speed
        if self.rect.y >= 440:
            self.kill()

class Barrier(pygame.sprite.Sprite):

    def __init__(self, pos, type):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.damage = 0
        self.sprites = barriers[type]
        self.image = self.sprites[self.damage]
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))
    
    def hit(self):
        self.damage += 1
        if self.damage == 4: 
            self.kill()
        else:
            self.image = self.sprites[self.damage]
