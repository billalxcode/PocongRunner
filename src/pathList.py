#== Import lib ==#
from os.path import join as JoinPath
from os.path import split as SplitPath
from os.path import abspath
from os.path import splitext
from os.path import basename
from os import listdir

#== Runtime path ==#
def runtime_path():
    path = SplitPath(abspath("__file__"))[0]
    return path

#== Get basename ==#
def get_name_file(filename):
    return splitext(basename(filename))[0]

#== Get filename extension ==#
def get_extension(filename):
    return splitext(filename)[1]

#== Background image ==#
BACKGROUND_IMAGE = [JoinPath(runtime_path(), "assets/images/background/" + file) for file in listdir(JoinPath(runtime_path(), "assets/images/background"))]

#== Texture image ==#
TEXTURE_IMAGE = [JoinPath(runtime_path(), "assets/images/texture/" + file) for file in listdir(JoinPath(runtime_path(), "assets/images/texture"))]

#== Icon image ==#
ICON_GAME = JoinPath(runtime_path(), "assets/images/anim/pocong1.png")

#== Anim image ===#
POCONG_IMAGE = JoinPath(runtime_path(), "assets/images/anim/player1.png")
KERIS_IMAGE = JoinPath(runtime_path(), "assets/images/anim/keris.png")

#== Other image ==#
OTHERS = [JoinPath(runtime_path(), "assets/images/utama/" + file) for file in listdir(JoinPath(runtime_path(), "assets/images/utama"))]

#== Fonts ==#
FONTS = []
for fonts in listdir(JoinPath(runtime_path(), "assets/fonts")):
    if get_extension(fonts) == ".ttf":
        FONTS.append(JoinPath(runtime_path(), "assets/fonts/" + fonts))


#== Sounds ==#
EFFECTS = []
for effect in listdir(JoinPath(runtime_path(), "assets/sound")):
    if "effects" in get_name_file(effect):
        EFFECTS.append(JoinPath(runtime_path(), "assets/sound/" + effect))

SOUND = []
for sounds in listdir(JoinPath(runtime_path(), "assets/sound")):
    if "sound" in get_name_file(sounds):
        SOUND.append(JoinPath(runtime_path(), "assets/sound/" + sounds))

#== Database ==#
DATABASE = JoinPath(runtime_path(), "assets/databases/games.db")

#== Config ==#
CONFIG_PATH = JoinPath(runtime_path(), "assets/config/config.json")