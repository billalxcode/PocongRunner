import sqlite3

from src.pathList import DATABASE
from src.logs import Logs

class Database:
    def __init__(self):
        self.path = DATABASE # Path database
        self.sql = None
        self.id = 1
        self.coint = 0
        self.name = "Ocong"

        self.logs = Logs()

    #=== Function connect to database ===#
    def connect(self):
        self.logs.info("Menghubungkan ke database")
        self.sql = sqlite3.connect(self.path)

    def getProfile(self):
        if self.sql:
            select = self.sql.execute("SELECT * FROM profile")
            for row in select:
                self.id = row[0]
                self.coint = row[1]
                self.name = row[2]
            return self.id, self.coint, self.name
        else:
            self.logs.error("Kamu belum menghubungkan ke database", keluar=True)

    def updateScore(self, score):
        if self.sql:
            id, coint, name = self.getProfile()
            c = self.sql.cursor()
            c.execute("UPDATE profile SET coint=%d WHERE id=%d" % (coint+score, id))
            self.sql.commit()
        else:
            self.logs.error("Kamu belum menghubungkan ke database")