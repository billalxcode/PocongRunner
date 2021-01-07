import pygame
from pygame.freetype import Font
from pygame.mask import from_surface
from pygame.mixer import Sound
from itertools import cycle

from src.utils import COLLECT_BACKSOUND

class Player(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = from_surface(self.image)
        self.rect.left, self.rect.top = position

        self.jump = False
        self.down = 0
        self.up = 0

    def update(self, boundary_values, time_passed):
        if self.jump:
            self.up -= 50 * time_passed
            self.rect.top -= self.up
            if self.up <= 0:
                self.jump2()
                self.up = 9
                self.down = 0
        else:
            if self.rect.bottom >= 450:
                self.rect.bottom = 450
            else:
                self.down += 20 * time_passed
                self.rect.bottom += self.down

    def set_jump(self):
        if self.jump:
            self.up = max(12, self.up+1)
        else:
            self.jump = True

    def jump2(self):
        self.jump = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Keris(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = from_surface(self.image)
        self.rect.left, top = position
        self.position = position
        self.is_used = False

    def set_position(self, new_position):
        self.position = new_position

    def draw(self, screen):
        screen.blit(self.image, self.position)

class Bambu(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = from_surface(self.image)
        self.rect.left, self.rect.top = position
        self.used_score = False

    def update(self, diff, old_position):
        # self.rect.left = -((-self.position[0] + 4) % diff)
        self.rect.left = -((-self.rect.left + 4) % diff)

        return (self.rect.left, self.rect.top)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Health(object):
    def __init__(self, image_bar, health, rect):
        self.value = 200
        self.health_bar = image_bar
        self.health = health
        self.width = rect.width

    def revalue(self):
        self.value -= 10

    def add_value(self):
        if self.value >= 200:
            self.value = 200
        else:
            self.value += 5

    def draw(self, screen):
        screen.blit(self.health_bar, (self.width-230, 5))
        for i in range(self.value):
            screen.blit(self.health, (i+(self.width-233), 8))

class Score(object):
    def __init__(self, font_path):
        self.collect = Sound(COLLECT_BACKSOUND)
        self.font = Font(font_path, 24)
        self.score = 0
        self.old_score = self.score

    def add_score(self):
        self.score += 1
        new_score = self.old_score + 10
        if self.score == new_score:
            self.collect.play()
            self.old_score = self.score

    def rescore(self):
        self.score -= 1

    def draw(self, screen):
        text_surface, rect = self.font.render("Score: " + str(self.score), (133, 230, 159))
        screen.blit(text_surface, (10,10))