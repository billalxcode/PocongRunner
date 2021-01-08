from pygame import init as PyGameInit
from pygame import error as PyGameErrorException
from pygame import quit as PyGameQuit
from pygame.transform import scale, rotate, flip
from pygame.display import update, set_caption, set_mode
from pygame.locals import Rect, KEYDOWN, KEYUP, QUIT, K_ESCAPE, K_SPACE
from pygame.event import get as PyGameEvent
from pygame.image import load as PyGameLoadImage
from pygame.time import Clock as PyGameclock
from pygame.surface import Surface as PyGameSurface
from pygame.sprite import Group as PyGameSpriteGroup
from pygame.sprite import collide_mask

from src.utils import BACKGROUND_GAME, BACKGROUND_START, STONE_IMAGE, PLAYER_IMAGE, KERIS_IMAGE, SCORE_FONT, BAMBU_IMAGE, HEALTH_IMAGE, HEALTHBAR_IMAGE, BACKGROUND_END
from src.startGame import StartGame
from src.endGame import EndGame
from src.core import Player, Keris, Score, Bambu, Health

import random

class Main(object):
    def __init__(self):
        self.rect = Rect(0, 0, 640, 480)
        self.gameover = False

    def load_image(self, path, convert_alpha=False, convert=True):
        try:
            resource = PyGameLoadImage(path)
        except PyGameErrorException:
            print ("duarrr")
            exit(0)
        if convert:
            return resource.convert()
        elif convert_alpha:
            return resource.convert_alpha()
        else:
            return resource

    def load_all_images(self):
        print (BACKGROUND_GAME)
        self.BACKGROUND_IMAGE = self.load_image(path=BACKGROUND_GAME, convert=False, convert_alpha=True)
        self.BACKGROUND_IMAGE = scale(self.BACKGROUND_IMAGE, (self.rect.width, self.BACKGROUND_IMAGE.get_height()))
        self.BACKGROUND_START = self.load_image(path=BACKGROUND_START, convert=False, convert_alpha=True)
        self.BACKGROUND_START = scale(self.BACKGROUND_START, (int(self.BACKGROUND_START.get_width()/2), self.rect.height))
        self.BACKGROUND_END = self.load_image(path=BACKGROUND_END, convert=False, convert_alpha=True)
        self.BACKGROUND_END = scale(self.BACKGROUND_END, (int(self.BACKGROUND_END.get_width()/2), self.rect.height))
        self.STONE_IMAGE = self.load_image(path=STONE_IMAGE, convert=True, convert_alpha=True)
        self.PLAYER_IMAGE = self.load_image(path=PLAYER_IMAGE, convert=False, convert_alpha=True)
        self.PLAYER_IMAGE = flip(self.PLAYER_IMAGE, True, False)
        self.PLAYER_IMAGE = scale(self.PLAYER_IMAGE, (100, 100))
        self.KERIS_IMAGE = self.load_image(path=KERIS_IMAGE, convert=False, convert_alpha=True)
        self.BAMBU_IMAGE = self.load_image(path=BAMBU_IMAGE, convert=False, convert_alpha=True)
        self.HEALTH_IMAGE = self.load_image(path=HEALTH_IMAGE, convert=False, convert_alpha=True)
        self.HEALTHBAR_IMAGE = self.load_image(path=HEALTHBAR_IMAGE, convert=False, convert_alpha=True)

    def setup(self):
        PyGameInit()
        set_caption("Pocong runner")
        self.screen = set_mode(self.rect.size)

        self.load_all_images()
        self.base_position = [0, self.rect.height*0.95]
        self.base_diff = self.STONE_IMAGE.get_width() - self.BACKGROUND_IMAGE.get_width()
        
        self.player = Player(self.PLAYER_IMAGE, [60, 450])

        self.keris_diff = self.KERIS_IMAGE.get_width() - self.BACKGROUND_IMAGE.get_width()
        self.kerisGroup = PyGameSpriteGroup()
        for idx in range(random.randint(1, 2)):
            keris_position = [self.rect.width+random.randint(10, 200), self.rect.height*0.80]
            keris = Keris(self.KERIS_IMAGE, keris_position)
            keris.rect.bottom += random.randint(100, self.rect.height-120)
            self.kerisGroup.add(keris)
        
        self.bambu_diff = self.BAMBU_IMAGE.get_width() - self.BACKGROUND_IMAGE.get_width()

        self.bambugroup = PyGameSpriteGroup()
        for x in range(random.randint(1, 3)):        
            self.bambuPosition = [random.randint(self.rect.width, 1000), self.rect.height*0.80]
            bambuEnemy = Bambu(self.BAMBU_IMAGE, self.bambuPosition)
            self.bambugroup.add(bambuEnemy)

        self.health = Health(self.HEALTHBAR_IMAGE, self.HEALTH_IMAGE, self.rect)

        self.score = Score(SCORE_FONT)
        self.clock = PyGameclock()

    def control(self):
        for event in PyGameEvent():
            if event.type == QUIT:
                self.gameover = True
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.player.set_jump()

    def run(self):
        self.setup()
        start = StartGame(self.screen, self.rect, self.BACKGROUND_START)
        if start.run():
            self.gameover = True

        is_add = True

        while not self.gameover:
            self.control()

            #== Check is game over ==#
            if self.score.check():
                self.gameover = True
            elif self.health.check():
                self.gameover = True

            self.base_position[0] = -((-self.base_position[0] + 4) % self.base_diff)
            
            boundary_values = [0, self.base_position[-1]]
            self.player.update(boundary_values, float(self.clock.tick(60)/1000))
            # self.bambuEnemy.update(self.bambu_diff, self.bambuPosition)

            flag = False
            for keris in self.kerisGroup:
                keris.rect.left -= 4
                if collide_mask(self.player, keris) and not keris.is_used:
                    keris.is_used = True
                    self.score.add_score()
                    self.kerisGroup.remove(keris)
                    self.health.add_value()
                    is_add = True
                
                if keris.rect.left < 5 and keris.rect.left > 0 and is_add:
                    self.health.revalue()
                    keris_position = [self.rect.width+random.randint(10, 200), self.rect.height*0.80]
                    new_keris = Keris(self.KERIS_IMAGE, keris_position)
                    new_keris.rect.bottom += random.randint(100, self.rect.height-120)
                    self.kerisGroup.add(new_keris)
                    is_add = False

                elif is_add and keris.is_used:
                    if random.randint(0, 1) == 1:
                        for _ in range(random.randint(1, 2)):
                            keris_position = [self.rect.width+random.randint(10, 200), self.rect.height*0.80]
                            new_keris = Keris(self.KERIS_IMAGE, keris_position)
                            new_keris.rect.bottom += random.randint(100, self.rect.height-120)
                            self.kerisGroup.add(new_keris)
                    else:
                        keris_position = [self.rect.width+random.randint(10, 200), self.rect.height*0.80]
                        new_keris = Keris(self.KERIS_IMAGE, keris_position)
                        new_keris.rect.bottom += random.randint(100, self.rect.height-120)
                        self.kerisGroup.add(new_keris)
                    is_add = False

                elif keris.rect.right < 0:
                    self.health.revalue()
                    self.kerisGroup.remove(keris)
                    is_add = True

            bambu_is_add = True
            for bambuEnemy in self.bambugroup:
                bambuEnemy.rect.left -= 4
                if collide_mask(self.player, bambuEnemy) and not bambuEnemy.used_score:
                    bambuEnemy.used_score = True
                    self.score.rescore()
                    self.health.revalue()
                    bambu_is_add = True

                if bambuEnemy.rect.left < 4 and self.rect.left > 0 and bambu_is_add:
                    bambuPosition = [random.randint(self.rect.width, 1000), self.rect.height*0.80]
                    bambu = Bambu(self.BAMBU_IMAGE, bambuPosition)
                    self.bambugroup.add(bambu)
                    bambu_is_add = False

                elif bambuEnemy.rect.right < 0:
                    self.bambugroup.remove(bambuEnemy)
                    bambuPosition = [random.randint(self.rect.width, 1000), self.rect.height*0.80]
                    bambu = Bambu(self.BAMBU_IMAGE, bambuPosition)
                    self.bambugroup.add(bambu)

            self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))
            self.screen.blit(self.STONE_IMAGE, self.base_position)
            self.bambugroup.draw(self.screen)
            self.kerisGroup.draw(self.screen)
            self.health.draw(self.screen)
            self.player.draw(self.screen)
            self.score.draw(self.screen)

            update()

            self.clock.tick(60)
        
        end = EndGame(self.screen, self.rect, self.BACKGROUND_END)
        end.run()
        PyGameQuit()