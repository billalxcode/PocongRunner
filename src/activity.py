#=== Import global packet ===#
import random
import pygame
from pygame.display import update, set_caption, set_mode, set_icon
from pygame.transform import scale, flip
from pygame.mouse import set_visible
from pygame.sprite import Group
from pygame.time import Clock
from pygame.sprite import collide_mask

#=== Import paket lokal ==#
from src.logs import Logs
from src.config import Config
from src.core import Core
from src.introGame import introGame
from src.anim import Player, Rumput, Keris, Keris, Score, Health, Bambu
from src.database import Database

class Acticity:
    def __init__(self):
        self.config = Config()
        self.core = Core()
        self.logs = Logs()
        self.database = Database()
        
        self.data = {} # Data assets
        self.running = True

    def setup(self):
        pygame.init()
        self.database.connect()
        self.config.read()
        self.data = self.core.get_data
        self.speed = self.config.parse["settings"]["speed"]

        set_caption(self.config.getName + " " + self.config.getVersion)
        self.screen = set_mode(self.config.getRect.size)
        self.core.load_assets()
        if self.data["icon"]:
            self.logs.info("Mengatur icon")
            set_icon(self.data["icon"])
        set_visible(True)
        self.clock = Clock()

        #=== Background game ===#
        self.BACKGROUND = self.data["backgrounds"][random.choice([x for x in self.data["backgrounds"]][1:])]
        self.BACKGROUND = scale(self.BACKGROUND, self.config.getRect.size)

        #=== Settings tanah texture ===#
        self.tanah = self.data["textures"]["tanah0"]
        self.tanah = scale(self.tanah, (1000, self.tanah.get_height()))
        self.tanah_diff = self.tanah.get_width() - self.BACKGROUND.get_width()
        self.tanah_position = [0, self.config.getRect.height*0.95]
        
        #=== Settings grass texture ===#
        self.grass = self.data["textures"]["grass0"]
        self.grass = scale(self.grass, (1000, 10))
        self.grass_diff = self.grass.get_width() - self.BACKGROUND.get_width()
        self.grass_position = [10, self.config.getRect.height*0.94]

        #=== Settings rumput texture ===#
        rumput_image_list = []
        for x in self.data["textures"]:
            if "rumput" in x:
                rumput_image_list.append(x)
        
        self.rumputGroup = Group()
        for x in range(random.randint(2, 4)):
            image = self.data["textures"]["rumput0"]
            self.rumputGroup.add(Rumput(image, [random.randint(self.config.getRect.width, 3000), self.config.getRect.height*0.80]))
            
        #=== Settings keris image ===#
        self.kerisGroup = Group()
        for x in range(random.randint(1, 3)):
            keris = Keris(self.data["anim"]["keris"], [random.randint(self.config.getRect.width, self.config.getRect.width*2), 10])
            keris.rect.bottom += random.randint(10, self.config.getRect.height-130)
            self.kerisGroup.add(keris)

        #=== Settings bambu image ===#
        self.bambuGroup = Group()
        for x in range(random.randint(1, 3)):
            bambu = Bambu(self.data["other"]["bambu"], [random.randint(self.config.getRect.width, self.config.getRect.width*2), 10])
            bambu.rect.bottom += self.config.getRect.height * 0.78
            self.bambuGroup.add(bambu)

        #=== Settings player image ===#
        self.player = Player(self.data["anim"]["player1"], [60, self.config.getRect.height-40])

        #=== Settings score ===#
        self.score = Score(self.data)

        #=== Health bar ===#
        self.health = Health(self.data)

    def run(self):
        self.setup()
        self.running = introGame(self.screen, self.data, self.database.getProfile())

        add_rumput = True
        add_keris = True
        add_bambu = True
        while self.running:
            events = self.core.events()
            if events["type"]["quit"]:
                self.running = False
                break
            elif events["type"]["keydown"]:
                if events["keys"]["space"] or events["keys"]["up"]:
                    self.player.jump_up()

            #=== Move position ===#
            boundary_values = [0, self.grass_position[-1]]
            self.player.update(boundary_values, float(self.clock.tick(self.config.parse["settings"]["frame"])/1000))
            self.tanah_position[0] = -((-self.tanah_position[0] + self.speed) % self.tanah_diff)
            self.grass_position[0] = -((-self.grass_position[0] + self.speed) % self.grass_diff)
            
            #=== Move rumput object ===#
            for rumput in self.rumputGroup:
                rumput.rect.left -= self.config.parse["settings"]["speed"]
                if rumput.rect.left < 4 and rumput.rect.left > 0 and add_rumput:
                    if len(self.rumputGroup) > 50: continue
                    else:
                        image = self.data["textures"]["rumput" + str(random.randint(1, 6))]
                        self.rumputGroup.add(Rumput(image, [random.randint(self.config.getRect.width, 3000), self.config.getRect.height*0.80]))
                elif rumput.rect.right < 0:
                    if len(self.rumputGroup) > 50: 
                        self.rumputGroup.remove(rumput)
                    else:
                        self.rumputGroup.remove(rumput)
                        image = self.data["textures"]["rumput" + str(random.randint(1, 6))]
                        self.rumputGroup.add(Rumput(image, [random.randint(self.config.getRect.width, 3000), self.config.getRect.height*0.80]))
                
            #=== Move keris object ===#
            for keris in self.kerisGroup:
                keris.rect.left -= self.config.parse["settings"]["speed"]
                #=== Check object to object ===#
                if collide_mask(self.player, keris) and not keris.is_used:
                    keris.is_used = True
                    self.kerisGroup.remove(keris)
                    add_keris = True
                    self.health.add_value()
                    if self.score.add_score():
                        self.running = False
                        break

                if keris.rect.left < 4 and keris.rect.left > 0 and add_keris:
                    if self.health.revalue():
                        self.running = False
                        break
                    keris = Keris(self.data["anim"]["keris"], [random.randint(self.config.getRect.width, self.config.getRect.width*2), 10])
                    keris.rect.bottom += random.randint(10, self.config.getRect.height-130)
                    self.kerisGroup.add(keris)
                    add_keris = False

                elif add_keris and keris.is_used:
                    if random.randint(0, 1) == 1:
                        for _ in range(random.randint(1, 2)):
                            keris = Keris(self.data["anim"]["keris"], [random.randint(self.config.getRect.width, self.config.getRect.width*2), 10])
                            keris.rect.bottom += random.randint(10, self.config.getRect.height-130)
                            self.kerisGroup.add(keris)
                    else:
                        keris = Keris(self.data["anim"]["keris"], [random.randint(self.config.getRect.width, self.config.getRect.width*2), 10])
                        keris.rect.bottom += random.randint(10, self.config.getRect.height-130)
                        self.kerisGroup.add(keris)
                    add_keris = False
                elif keris.rect.right < 0:
                    self.health.revalue()
                    self.kerisGroup.remove(keris)
                    keris = Keris(self.data["anim"]["keris"], [random.randint(self.config.getRect.width, self.config.getRect.width*2), 10])
                    keris.rect.bottom += random.randint(10, self.config.getRect.height-130)
                    self.kerisGroup.add(keris)
                
            for bambuEnemy in self.bambuGroup:
                bambuEnemy.rect.left -= self.config.parse["settings"]["speed"]
                if collide_mask(self.player, bambuEnemy) and not bambuEnemy.is_used:
                    bambuEnemy.is_used = True
                    add_bambu = True
                    self.health.revalue()
                    self.score.rescore()

                if bambuEnemy.rect.left < 4 and bambuEnemy.rect.left > 0 and add_bambu:
                    bambu = Bambu(self.data["other"]["bambu"], [random.randint(self.config.getRect.width, self.config.getRect.width*2), 10])
                    bambu.rect.bottom += self.config.getRect.height * 0.78
                    self.bambuGroup.add(bambu)
                    add_bambu = False
                
                elif bambuEnemy.rect.right < 0:
                    self.bambuGroup.remove(bambuEnemy)
                    bambu = Bambu(self.data["other"]["bambu"], [random.randint(self.config.getRect.width, self.config.getRect.width*2), 10])
                    bambu.rect.bottom += self.config.getRect.height * 0.78
                    self.bambuGroup.add(bambu) 

            #=== Screen display ===#
            self.screen.blit(self.BACKGROUND, (0, 0))
            self.rumputGroup.draw(self.screen)
            self.screen.blit(self.tanah, self.tanah_position)
            self.screen.blit(self.grass, self.grass_position)
            self.bambuGroup.draw(self.screen)
            self.health.draw(self.screen)
            self.kerisGroup.draw(self.screen)
            self.player.draw(self.screen)
            self.score.draw(self.screen)

            #=== Check ===#
            if self.score.check():
                self.running = False
            elif self.health.check():
                self.running = False
            self.clock.tick(self.config.parse["settings"]["frame"])
            update()
        self.logs.warning("Menyimpan score")
        self.database.updateScore(self.score.getScore)
        self.logs.warning("Menutup game...")
        pygame.quit()