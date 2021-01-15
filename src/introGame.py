from pygame.display import update
from pygame.transform import scale
from pygame.mouse import get_pos
from pygame.surface import Surface
from pygame.freetype import Font

from src.config import Config
from src.core import Core
from src.logs import Logs

config = Config()
core = Core()
logs = Logs()

def introGame(screen, asset, data):
    #=== Background image ===#
    logs.info("Mengatur latar belakang...")
    bg = scale(asset["backgrounds"]["intro"], (config.getRect.size))

    #=== Button play image ===#
    logs.info("Mengatur button...")
    btn_play = asset["other"]["btn-play2"]
    btn_play = scale(btn_play, (int(btn_play.get_width()/2), btn_play.get_height()-100))
    btn_play_center = btn_play.get_rect()
    btn_play_center.center = config.getRect.center

    #=== button keluar  image ===#
    btn_keluar = asset["other"]["btn-keluar2"]
    btn_keluar = scale(btn_keluar, (int(btn_keluar.get_width()/2), btn_keluar.get_height()-100))
    btn_keluar_center = btn_keluar.get_rect()
    btn_keluar_center.center = config.getRect.center
    btn_keluar_center.bottom += 100

    #=== Button settings image ===#
    btn_settings = asset["other"]["btn-settings2"]
    btn_settings = scale(btn_settings, (int(btn_settings.get_width()/2), btn_settings.get_height()-100))
    btn_settings_center = btn_settings.get_rect()
    btn_settings_center.center = config.getRect.center
    btn_settings_center.bottom += 50

    #=== Button credits image ===#
    btn_credits = asset["other"]["btn-credits"]
    btn_credits = scale(btn_credits, (100, 100))
    btn_credits_center = btn_credits.get_rect()
    btn_credits_center.center = config.getRect.center
    btn_credits_center.bottom = config.getRect.height
    btn_credits_center.right = config.getRect.width

    btn_close = asset["other"]["btn-close"]
    btn_close = scale(btn_close, (100, 100))
    btn_close_center = btn_close.get_rect()
    btn_close_center.center = config.getRect.center
    btn_close_center.bottom = config.getRect.height
    btn_close_center.right = config.getRect.width
    
    #=== Settings coint image ===#
    coint_image = asset["other"]["coint"]
    coint_image = scale(coint_image, (40, 40))
    coint_image.set_colorkey("black")
    coint_rect = coint_image.get_rect()
    
    #=== Window credit image ===#
    win_credits = asset["other"]["credits2"]
    win_credits = scale(win_credits, (500, 500))
    win_credits.set_colorkey("black")
    win_credits_center = win_credits.get_rect()
    win_credits_center.center = config.getRect.center
    
    #=== Font warning ===#
    logs.info("Mengatur teks peringatan")
    info = Font(asset["fonts"]["AboveDemoRegular-lJMd"], 10)
    info_text, info_rect = info.render("*Jika anda mengklaim pemilik dari asset game ini, silahkan hubungi pembuat.", (255,255,255))
    info_rect.bottom = config.getRect.height

    #=== Font coint ===#
    logs.info("Mengatur teks coint")
    id, coint, name = data
    font_coint = Font(asset["fonts"]["PressStart2P"], 20)
    coint_text, coint_text_rect = font_coint.render(str(coint), (255,255,255))
    coint_text_rect.bottom = 28
    coint_text_rect.right += 45

    credit_window = False

    running = True
    while running:
        events = core.events()
        if events["type"]["quit"]:
            return False
        elif events["type"]["mousedown"]:
            if events["keys"]["button"] == 1:
                if not credit_window:
                    if btn_play_center.collidepoint(get_pos()):
                        asset["effects"]["click-effects"].play()
                        return True
                    elif btn_settings_center.collidepoint(get_pos()):
                        asset["effects"]["click-effects"].play()
                        credit_window = True
                    elif btn_keluar_center.collidepoint(get_pos()):
                        asset["effects"]["click-effects"].play()
                        return False
                    elif btn_credits_center.collidepoint(get_pos()):
                        asset["effects"]["click-effects"].play()
                        credit_window = True
                else:
                    if btn_close_center.collidepoint(get_pos()):
                        asset["effects"]["click-effects"].play()
                        credit_window = False
                        
        screen.blit(bg, (0, 0))
        if credit_window:
            screen.blit(win_credits, win_credits_center)
            screen.blit(btn_close, btn_close_center)
        else:
            screen.blit(btn_play, btn_play_center)
            screen.blit(btn_keluar, btn_keluar_center)
            screen.blit(btn_settings, btn_settings_center)
            screen.blit(btn_credits, btn_credits_center)
            screen.blit(coint_image, coint_rect)
            screen.blit(coint_text, coint_text_rect)
        screen.blit(info_text, info_rect)
        update()