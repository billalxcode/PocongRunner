import pygame
from pygame.mask import from_surface
from pygame.freetype import Font
from pygame.transform import scale

from src.config import Config

class Player(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)

        image = scale(image, (100, 100))
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = from_surface(self.image)
        self.rect.left, self.rect.top = position

        self.jump = False
        self.down = 0
        self.up = 0

        self.config = Config()
        self.bottom = self.config.getRect.bottom - 40

    def update(self, boundary_values, time_passed):
        if self.jump:
            self.up -= 50 * time_passed
            self.rect.top -= self.up
            if self.up <= 0:
                self.jump_down()
                self.up = 9
                self.down = 0
            if self.rect.top <= 0:
                self.rect.top = 0
        else:
            if self.rect.bottom >= self.bottom:
                self.rect.bottom = self.bottom
            else:
                self.down += 20 * time_passed
                self.rect.bottom += self.down

    def jump_up(self):
        if self.jump:
            self.up = max(12, self.up+1)
        else:
            self.jump = True

    def jump_down(self):
        self.jump = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Rumput(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = from_surface(self.image)
        self.rect.left, self.rect.top = position

class Keris(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.mask = from_surface(self.image)
        self.rect.left, self.rect.top = position
        self.is_used = False

class Bambu(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.mask = from_surface(self.image)
        self.rect.left, self.rect.top = position
        self.is_used = False

class Score(object):
    def __init__(self, asset):
        self.score = 0
        self.old_score = self.score
        
        self.collect = asset["effects"]["collects-effects"]
        self.font = Font(asset["fonts"]["CursedTimerUlil-Aznm"], 20)

    @property
    def getScore(self):
        return self.score
        
    def check(self):
        if self.score < 0:
            return True

    def add_score(self):
        self.score += 1
        new_score = self.old_score + 10
        if self.score == new_score:
            self.collect.play()
            self.old_score = self.score

    def rescore(self):
        self.score -= 1

    def draw(self, screen):
        text, rect = self.font.render("Skor: " + str(self.score), (133,230, 159))
        screen.blit(text, rect)

class Health(object):
    def __init__(self, asset):
        self.config = Config()
        self.config.read()

        self.value = 200
        self.healthbar = asset["other"]["healthbar"]
        self.health = asset["other"]["health"]
        
        self.healthbar_rect = self.healthbar.get_rect()
        self.healthbar_rect.right = self.config.getRect.width-40

        self.health_rect = self.health.get_rect()
        self.health_rect.right = self.config.getRect.width-43
        self.health_rect.right -= 43
        
    def check(self):
        if self.value < 0:
            return True
            
    def revalue(self):
        self.value -= 20

    def add_value(self):
        if self.value >= 200:
            self.value = 200
        else:
            self.value += 5

    def draw(self, screen):
        screen.blit(self.healthbar, (self.config.getRect.width-227, 5))
        for i in range(self.value):
            screen.blit(self.health, (i+(self.config.getRect.width-230), 8))