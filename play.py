import pygame, os
import numpy as np
from entities import *
from enemies import *

import copy

pygame.init()
clock = pygame.time.Clock()
fps = 60
screenWidth = 730
screenHeight = 500
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Space Invaders")
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
player = Player((365, 440))
all_sprites.add(player)


def setup():
    x_delta = 45
    y_delta = 35
    x_pos = 25
    y_pos = 75
    for i in range(11):
        e1 = SmallEnemy((x_pos, y_pos))
        e2 = MediumEnemy((x_pos, y_pos + y_delta))
        e3 = MediumEnemy((x_pos, y_pos + y_delta * 2))
        e4 = LargeEnemy((x_pos, y_pos + y_delta * 3))
        e5 = LargeEnemy((x_pos, y_pos + y_delta * 4))
        enemy_sprites.add(e1, e2, e3, e4, e5)
        all_sprites.add(e1, e2, e3, e4, e5)
        x_pos += x_delta


def play():
    setup()
    running = True
    projectile_spawned = False
    image_update_countdown = fps/2
    moving_counter = 34
    current_direction = "right"
    moving_down = False

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            if player.rect.x + player.rect.size[0] < screenWidth:
                player.move(6)
            else:
                player.rect.x = screenWidth - player.rect.size[0]
        if key_pressed[pygame.K_LEFT]:
            if player.rect.x - 5 >= 0:
                player.move(-6)
            else:
                player.rect.x = 0
        if key_pressed[pygame.K_SPACE] and projectile_spawned == False:
            projectile = PlayerProjectile(
                (int(player.rect.x + player.rect.size[0] / 2), int(player.rect.y - player.rect.size[1])))
            all_sprites.add(projectile)
            projectile_spawned = True

        if projectile_spawned:
            enemy = pygame.sprite.spritecollideany(projectile, enemy_sprites)
            if enemy is not None:
                enemy.hit()
                enemy.update()
                projectile_spawned = False
                projectile.kill()
            else:
                projectile.move(7)
                if projectile.rect.y <= 0:
                    projectile_spawned = False
                    projectile.kill()

        image_update_countdown -= 1
        if image_update_countdown <= 0:
            if moving_down:
                if current_direction == "right":
                    current_direction = "left"
                else:
                    current_direction = "right"
                for enemy in enemy_sprites.sprites():
                    enemy.direction = current_direction
                moving_down = False
            else:
                moving_counter -= 1
                if moving_counter == 0:
                    moving_down = True
                    for enemy in enemy_sprites.sprites():
                        enemy.direction = "down"
                    moving_counter = 34
            enemy_sprites.update()
            image_update_countdown = fps/2

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)

play()
