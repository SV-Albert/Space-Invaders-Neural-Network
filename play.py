import pygame, os
from entities import *
from enemies import *

# Some fileds
shooting_chance = 0.75
fps = 60
update_delay = fps/4
screenWidth = 730
screenHeight = 500

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Space Invaders")
foreground_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
enemy_projectiles = pygame.sprite.Group()
player = Player((365, 440))
foreground_sprites.add(player)

bottom_line = pygame.Rect(0, 450, screenWidth, 4)
player_image = pygame.image.load(os.path.join(os.sys.path[0], "Assets", "player.png"))
font = pygame.font.SysFont('Impact', 22)

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
        foreground_sprites.add(e1, e2, e3, e4, e5)
        x_pos += x_delta


def play():
    setup()
    lives = 3
    score = 0
    running = True
    projectile_spawned = False
    update_countdown = update_delay
    moving_counter = 34
    lane = 11
    current_direction = "right"
    moving_down = False

    while running:
        screen.fill((0, 0, 0))
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

        # Code for the player projectiles 
        if projectile_spawned:
            missle = pygame.sprite.spritecollideany(projectile, enemy_projectiles)
            if missle is not None:
                missle.kill()
                projectile_spawned = False
                projectile.kill()

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

        missle = pygame.sprite.spritecollideany(player, enemy_projectiles)
        if missle is not None:
            lives -= 1
            missle.kill()
            if lives < 0: 
                running = False

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
            update_countdown = update_delay

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
        screen.blit(score_text, (20, 15))
        pygame.display.flip()
        clock.tick(fps)

play()
