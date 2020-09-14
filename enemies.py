import pygame, os, random

mystery_speed = 4

def loadSprite(name):
    sprite_location = os.path.join(os.sys.path[0], "Assets", name)
    return pygame.image.load(sprite_location).convert()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.isDead = False
        self.direction = "right"

    def update(self):
        if self.isDead:
            if pygame.time.get_ticks() - self.deathTimer > 50:  # Death animation length
                self.kill()
        else:
            if self.currentSprite == 0:
                self.image = self.sprites[1]
                self.currentSprite = 1
            else:
                self.image = self.sprites[0]
                self.currentSprite = 0

            if self.direction == "right":
                self.rect.x += 7
            elif self.direction == "left":
                self.rect.x -= 7
            elif self.direction == "down":
                self.rect.y += 15

    def hit(self):
        sprite_center = self.rect.center
        sprite_location = os.path.join(os.sys.path[0], "Assets", "explosion.png")
        sprite_image = pygame.image.load(sprite_location)
        self.image = sprite_image.convert()
        self.rect = sprite_image.get_rect(center=sprite_center)
        self.isDead = True
        self.deathTimer = pygame.time.get_ticks()
        super().update()


class LargeEnemy(Enemy):
    def __init__(self, pos):
        super().__init__(pos)
        self.sprites = [loadSprite("large1.png"), loadSprite("large2.png")]
        self.score_worth = 10
        self.currentSprite = 0
        self.image = self.sprites[0]
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))


class MediumEnemy(Enemy):
    def __init__(self, pos):
        super().__init__(pos)
        self.sprites = [loadSprite("medium1.png"), loadSprite("medium2.png")]
        self.score_worth = 20
        self.currentSprite = 0
        self.image = self.sprites[0]
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))


class SmallEnemy(Enemy):
    def __init__(self, pos):
        super().__init__(pos)
        self.sprites = [loadSprite("small1.png"), loadSprite("small2.png")]
        self.score_worth = 30
        self.currentSprite = 0
        self.image = self.sprites[0]
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))

class MysteryEnemy(Enemy):
    def __init__(self):
        super().__init__((730, 40))
        self.sprites = [loadSprite("mystery.png")]
        # self.score_worth = 30
        self.currentSprite = 0
        self.image = self.sprites[0]
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))

    def update(self):
        if self.isDead:
            if pygame.time.get_ticks() - self.deathTimer > 50:  # Death animation length
                self.kill()
        elif self.rect.x + self.rect.size[0] <= 0: 
            self.kill()
        else: 
            self.rect.x -= mystery_speed