import pygame, os
pygame.init()
screenWidth = 730
screenHeight = 500
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

from entities import *
from enemies import *

# Some fileds
shooting_chance = 0.75
mystery_chance = 0.001
fps = 60

foreground_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
enemy_projectiles = pygame.sprite.Group()
barrier_sprites = pygame.sprite.Group()
player = Player((365, 440))
foreground_sprites.add(player)

bottom_line = pygame.Rect(0, 450, screenWidth, 4)
player_image = pygame.image.load(os.path.join(os.sys.path[0], "Assets", "player.png"))
background = pygame.image.load(os.path.join(os.sys.path[0], "Assets", "background.jpg"))
font = pygame.font.SysFont('Impact', 25)

def setup():
    x_delta = 45
    y_delta = 35
    x_pos = 25
    y_pos = 70
    for i in range(11):
        e0 = SmallEnemy((x_pos, y_pos))
        e1 = MediumEnemy((x_pos, y_pos + y_delta))
        e2 = MediumEnemy((x_pos, y_pos + y_delta * 2))
        e3 = LargeEnemy((x_pos, y_pos + y_delta * 3))
        e4 = LargeEnemy((x_pos, y_pos + y_delta * 4))
        enemy_sprites.add(e0, e1, e2, e3, e4)
        foreground_sprites.add(e0, e1, e2, e3, e4)
        x_pos += x_delta

    delta = 20
    x_pos = 70
    y_pos = 365
    for i in range(4):
        b0 = Barrier((x_pos, y_pos), 2)
        b1 = Barrier((x_pos + delta, y_pos), 0)
        b2 = Barrier((x_pos + delta * 2, y_pos), 0)
        b3 = Barrier((x_pos + delta * 3, y_pos), 1)
        b4 = Barrier((x_pos, y_pos + delta), 0)
        b5 = Barrier((x_pos + delta, y_pos + delta), 3)
        b6 = Barrier((x_pos + delta * 2, y_pos + delta), 4)
        b7 = Barrier((x_pos + delta * 3, y_pos + delta), 0)
        b8 = Barrier((x_pos, y_pos + delta * 2), 0)
        b9 = Barrier((x_pos + delta * 3, y_pos + delta * 2), 0)
        barrier_sprites.add(b0, b1, b2, b3, b4, b5, b6, b7, b8, b9)
        foreground_sprites.add(b0, b1, b2, b3, b4, b5, b6, b7, b8, b9)
        x_pos += 170

def play():
    setup()
    lives = 3
    score = 0
    shots_fired = 0
    running = True
    projectile_spawned = False
    mystery_spawned = False
    update_countdown = int(len(enemy_sprites.sprites())/2)
    moving_counter = 34
    lane = 11
    current_direction = "right"
    moving_down = False

    while running:
        screen.blit(background, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        # Key press event handling 
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
            projectile = PlayerProjectile((player.rect.center[0], player.rect.center[1]))
            foreground_sprites.add(projectile)
            projectile_spawned = True
            shots_fired += 1

        # Spawn mystery ship
        if not mystery_spawned and random.uniform(0,1) < mystery_chance: 
            mystery_spawned = True
            mystery_ship = MysteryEnemy()
            foreground_sprites.add(mystery_ship)

        # Code for the player projectiles 
        if projectile_spawned:
            # Collision between player projectile and missles
            missle = pygame.sprite.spritecollideany(projectile, enemy_projectiles)
            if missle is not None:
                missle.kill()
                projectile_spawned = False
                projectile.kill()
            # Collision between player projectile and the mystery ship
            if mystery_spawned:
                collision = pygame.sprite.collide_rect(mystery_ship, projectile)
                if collision:
                    mystery_spawned = False
                    mystery_ship.hit()
                    projectile_spawned = False
                    projectile.kill()
                    if shots_fired == 23 or shots_fired % 15 == 0:
                        score += 300
                    else:
                        possible_scores = [50, 100, 150]
                        score += possible_scores[random.randint(0,2)]
            # Collision between player projectile and barriers
            barrier = pygame.sprite.spritecollideany(projectile, barrier_sprites)
            if barrier is not None:
                barrier.hit()
                projectile_spawned = False
                projectile.kill()
            # Collision between player projectile and enemies
            enemy = pygame.sprite.spritecollideany(projectile, enemy_sprites)
            if enemy is not None:
                enemy.hit()
                score += enemy.score_worth
                projectile_spawned = False
                projectile.kill()
            else:
                projectile.update()
                if projectile.rect.y <= 0:
                    projectile_spawned = False
                    projectile.kill()

        # Collision between player and missles
        missle = pygame.sprite.spritecollideany(player, enemy_projectiles)
        if missle is not None:
            lives -= 1
            missle.kill()
            if lives == 0: 
                running = False
        # Collision between missles and barriers
        for missle in enemy_projectiles.sprites():
            barrier = pygame.sprite.spritecollideany(missle, barrier_sprites)
            if barrier is not None: 
                barrier.hit()
                missle.kill()

        # Update the sprites
        update_countdown -= 1
        if update_countdown <= 0:
            if random.uniform(0,1) < shooting_chance:
                index = random.randint(0, len(enemy_sprites.sprites()) - 1)
                enemy = enemy_sprites.sprites()[index]
                missle = EnemyProjectile((enemy.rect.center[0], enemy.rect.y + enemy.rect.size[1]))
                enemy_projectiles.add(missle)

            if moving_down:
                if current_direction == "right":
                    current_direction = "left"
                else:
                    current_direction = "right"
                for enemy in enemy_sprites.sprites():
                    enemy.direction = current_direction
                moving_down = False
                lane -= 1
                if lane == 0: 
                    running = False
                    break
            else:
                moving_counter -= 1
                if moving_counter == 0:
                    moving_down = True
                    for enemy in enemy_sprites.sprites():
                        enemy.direction = "down"
                    moving_counter = 34
            enemy_sprites.update()
            if int(len(enemy_sprites.sprites())/2) < 12:
                update_countdown = 12
            else:
                update_countdown = int(len(enemy_sprites.sprites())/3)

        if mystery_spawned:
            mystery_ship.update()
        enemy_projectiles.update()
        enemy_projectiles.draw(screen)
        foreground_sprites.draw(screen)

        pygame.draw.rect(screen, (255, 255, 255), bottom_line)
        # Display remaining lives
        x_pos = 30
        y_pos = 465
        for l in range(lives):
            screen.blit(player_image, (x_pos, y_pos))
            x_pos += 50
        
        score_text = font.render("Score: " + str(score), 1, (255, 255, 255))
        screen.blit(score_text, (600, 460))
        pygame.display.flip()
        clock.tick(fps)

play()
