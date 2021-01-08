from pygame import quit as PyGameQuit
from pygame import USEREVENT
from pygame.freetype import Font
from pygame.event import get
from pygame.time import Clock, set_timer
from pygame.image import load as PyGameImageLoad
from pygame.locals import QUIT, K_SPACE, KEYDOWN, K_KP_ENTER
from pygame.display import update
from pygame.surface import Surface
from pygame.mixer import init, music, Sound

from itertools import cycle
from src.utils import BACKGROUND_START, TITLE_FONT, PRESS_START_FONT, INFORMATION_FONT, GAMELAN_BACKSOUND, CLICK_BACKSOUND

class EndGame(object):
    def __init__(self, screen, rect, background):
        init()
        self.screen = screen
        self.rect = rect
        self.background = background
        self.font = Font(TITLE_FONT, 40)
        self.font_start = Font(PRESS_START_FONT, 15)
        self.font_author = Font(PRESS_START_FONT, 12)
        self.font_information = Font(INFORMATION_FONT, 8)
        self.gamelan_music = music.load(GAMELAN_BACKSOUND)
        self.click_sound = Sound(CLICK_BACKSOUND)

    def load_image(self, path, convert_alpha=False, convert=True):
        try:
            resource = PyGameImageLoad(path)
        except PyGameErrorException:
            print ("duarrr")
            exit(0)
        if convert:
            return resource.convert()
        elif convert_alpha:
            return resource.convert_alpha()
        else:
            return resource

    def run(self):
        clock = Clock()
        music.play()
        text_surface, rect = self.font.render("Pocong Runner", (150,51,51))
        author_surface, author_rect = self.font_author.render("@billalxcode", (255,255,255))
        author_rect.center = self.rect.center
        author_rect.bottom += 165
        
        start_text_surface, start_rect = self.font_start.render("Tekan enter untuk keluar....", (255,255,255))
        info_surface, info_rect = self.font_information.render("* Jika anda mengklaim pemilik dari font/gambar silahkan chat pembuat. Terima kasih telah mendukung saya.", (255,255,255))
        info_rect.bottom += self.rect.height - 20
        blink_rect = start_rect
        blink_rect.center = self.rect.center
        blink_rect.bottom += 150

        while True:
            for event in get():
                if event.type == QUIT:
                    return True
                elif event.type == KEYDOWN:
                    self.click_sound.play()
                    if event.key == K_SPACE or event.key == 13:
                        return False
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(author_surface,  author_rect)
            self.screen.blit(text_surface.convert_alpha(), (self.rect.width/2, 100))
            self.screen.blit(start_text_surface, blink_rect)
            self.screen.blit(info_surface, info_rect)
            clock.tick(60)

            update()