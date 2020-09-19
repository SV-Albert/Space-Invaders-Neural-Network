import pygame

movement_speed = 5

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15, 15))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(x = pos[0], y = pos[1])
    
    def update(self):
        self.rect.x -= movement_speed
        if self.rect.x <= 0: self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 30))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] 
        self.rect.y = pos[1]
    