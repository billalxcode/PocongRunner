from os.path import abspath
from os.path import join as JoinPath
from os.path import split as SplitPath

def getcwd():
    return SplitPath(abspath("__file__"))[0]

SCORE_FONT = JoinPath(getcwd() + "/assets/fonts/CursedTimerUlil-Aznm.ttf")
TITLE_FONT = JoinPath(getcwd() + "/assets/fonts/Blood Thirst.ttf")
PRESS_START_FONT = JoinPath(getcwd() + "/assets/fonts/PressStart2P.ttf")
INFORMATION_FONT = JoinPath(getcwd() + "/assets/fonts/AboveDemoRegular-lJMd.ttf")
BACKGROUND_GAME = JoinPath(getcwd() + "/assets/images/background2.png")
BACKGROUND_START = JoinPath(getcwd() + "/assets/images/background.png")
BACKGROUND_END = JoinPath(getcwd() + "/assets/images/background3.png")
STONE_IMAGE = JoinPath(getcwd() + "/assets/images/stone.jpg")
PLAYER_IMAGE = JoinPath(getcwd() + "/assets/images/player.png")
KERIS_IMAGE = JoinPath(getcwd() + "/assets/images/keris.png")
BAMBU_IMAGE = JoinPath(getcwd() + "/assets/images/bambu.png")
HEALTHBAR_IMAGE = JoinPath(getcwd() + "/assets/images/healthbar.png")
HEALTH_IMAGE = JoinPath(getcwd() + "/assets/images/health.png")
GAMELAN_BACKSOUND = JoinPath(getcwd() + "/assets/sound/backsound-start.ogg")
CLICK_BACKSOUND = JoinPath(getcwd() + "/assets/sound/click.ogg")
COLLECT_BACKSOUND = JoinPath(getcwd() + "/assets/sound/collect key.ogg")