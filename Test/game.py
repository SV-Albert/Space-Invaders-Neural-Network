import pygame, random
from objects import *

pygame.init()
screen = pygame.display.set_mode((400, 150))
pygame.display.set_caption("Test game")
clock = pygame.time.Clock()
fps = 60

font = pygame.font.SysFont('Comic Sans MS', 18)

player_x = 30
player_y = 120
player = Player((player_x, player_y))
player_sprite = pygame.sprite.GroupSingle()
player_sprite.add(player)
obst = pygame.sprite.GroupSingle()
spawn_chance = 0.05

jump_limit = 60

def play():
    score = 0
    countdown = 0
    reached_top = False
    running = True
    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        if obst.sprite == None and countdown <= 0 and random.uniform(0,1) < spawn_chance:
            obstacle = Obstacle((400, 135))
            obst.add(obstacle)
        else:
            countdown -= 1
        
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE] and player.rect.y > jump_limit and not reached_top:
            player.rect.y = player.rect.y - 5
            if player.rect.y <= jump_limit:
                reached_top = True
        elif player.rect.y <= player_y:
            player.rect.y = player.rect.y + 5

        if reached_top and player.rect.y == player_y:
            reached_top = False

        if pygame.sprite.spritecollideany(player, obst) is not None:
            running = False


        countdown -= 1
        score += 0.1
        score_text = font.render("Score: " + str(int(score)), 1, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        obst.update()
        obst.draw(screen)
        player_sprite.draw(screen)
        pygame.display.flip()
        clock.tick(fps)

play()