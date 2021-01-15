#=== Global packet ===#
from pygame import error
from pygame.image import load
from pygame.event import get
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_UP, K_SPACE
from pygame.mixer import Sound
from pygame.transform import flip

#=== Paket lokal ===#
from src.pathList import *
from src.logs import Logs
from src.config import Config

class Core:
    def __init__(self):
        self.logs = Logs()

        self.data = {
            "backgrounds": {},
            "textures": {},
            "anim": {},
            "other": {},
            "sounds": {},
            "effects": {},
            "fonts": {},
            "icon": False
        }

        self.config = Config()
        self.config.read()

    @property
    def get_data(self):
        return self.data

    def read(self, path="", convert=False, convert_alpha=False):
        #=== Load image ===#
        try:
            resource = load(path)
        except error:
            self.logs.error("Tidak dapat memuat gambar! " + path, keluar=True)
        if convert:
            return resource.convert()
        elif convert_alpha:
            return resource.convert_alpha()
        else:
            return resource

    def load_assets(self):
        #=== Load background asset ===#
        for background in BACKGROUND_IMAGE:
            name = get_name_file(background)
            image = self.read(path=background, convert_alpha=True, convert=False)
            self.data["backgrounds"][name] = image

        #=== Load texture asset ===#
        for texture in TEXTURE_IMAGE:
            name = get_name_file(texture)
            image = self.read(path=texture, convert_alpha=True, convert=False)
            self.data["textures"][name] = image

        #=== Load anim asset ===#
        pocng_name = get_name_file(POCONG_IMAGE)
        print (POCONG_IMAGE)
        image = self.read(path=POCONG_IMAGE, convert_alpha=True, convert=False)
        self.data["anim"][pocng_name] = flip(image, True, False)
        
        keris_name = get_name_file(KERIS_IMAGE)
        image = self.read(path=KERIS_IMAGE, convert_alpha=True, convert=False)
        self.data["anim"][keris_name] = image

        #=== Load other asset ===#
        for other in OTHERS:
            name = get_name_file(other)
            image = self.read(path=other, convert_alpha=True, convert=False)
            self.data["other"][name] = image

        #=== Load sound asset ===#
        for sound_file in SOUND:
            name = get_name_file(sound_file)
            sound = Sound(sound_file)
            
            self.data["sounds"][name] = sound

        #=== Load effects asset ===#
        for effects_file in EFFECTS:
            name = get_name_file(effects_file)
            sound = Sound(effects_file)
            sound.set_volume(self.config.parse["settings"]["volume"]/10)
            self.data["effects"][name] = sound

        #=== Load fonts ===#
        for fonts in FONTS:
            name = get_name_file(fonts)
            self.data["fonts"][name] = fonts

        self.data["icon"] = self.read(path=ICON_GAME, convert_alpha=True, convert=False)

    def events(self):
        events_dict = {"type": {"quit": False, "keydown": False, "keyup": False, "mousedown": False}, "keys": {"ESC": False, "space": False, "up": False, "button": 0}}
        for event in get():
            if event.type == QUIT:
                events_dict["type"]["quit"] = True
            elif event.type == MOUSEBUTTONDOWN:
                events_dict["type"]["mousedown"] = True
                if event.button == 1:
                    events_dict["keys"]["button"] = 1
                elif event.button == 2:
                    events_dict["keys"]["button"] = 2
                elif event.button == 3:
                    events_dict["keys"]["button"] = 3
            elif event.type == KEYDOWN:
                events_dict["type"]["keydown"] = True
                if event.key == K_SPACE:
                    events_dict["keys"]["space"] = True
                elif event.key == K_UP:
                    events_dict["keys"]["up"] = True
        return events_dict