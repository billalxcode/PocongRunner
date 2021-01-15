import json
from pygame.locals import Rect

from src.pathList import CONFIG_PATH
from src.logs import Logs

class Config(object):
    def __init__(self):
        super().__init__()

        self.logs = Logs() # Funtion logs

        self.path = CONFIG_PATH # config path
        self.data = {} # data (null)

        self.rect = Rect(0, 0, 960, 540)

    @property
    def parse(self):
        #=== parse data ===#
        return self.data

    @property
    def getVersion(self):
        try:
            return str(self.data["informations"]["version"])
        except KeyError:
            self.logs.error("Tidak dapat mengambil data!", keluar=True)

    @property
    def getName(self):
        try:
            return self.data["informations"]["name"]
        except KeyError:
            self.logs.error("Tidak dapat mengambil data!", keluar=True)

    @property
    def getInformation(self):
        #=== get information from config ===#
        try:
            return self.data["informations"]
        except KeyError:
            self.logs.error("Tidak dapat mengambil data!", keluar=True)

    @property
    def getRect(self):
        return self.rect

    def read(self):
        #==== membaca config ====#
        try:
            buka = open(self.path, "r").read()
            self.data = json.loads(buka)
            return True
        except IOError:
            self.logs.error("Tidak dapat membuka config!", keluar=True)
            return False