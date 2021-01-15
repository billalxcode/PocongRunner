from datetime import datetime
from sys import exit as Exit

class Timer:
    def __init__(self):
        super().__init__()

        self.now = datetime.now()
        
    def getTime(self):
        hour = self.now.hour
        minute = self.now.minute
        second = self.now.second
        if len(str(hour)) == 1: hour = "0" + str(hour)
        if len(str(minute)) == 1: minute = "0" + str(minute)
        if len(str(second)) == 1: second = "0" + str(second)

        timer = str(hour) + ":" + str(minute) + ":" + str(second)
        return timer

class Logs:
    def __init__(self):
        super().__init__()

        self.text = ""
        self.timer = Timer()
        
    def reset(self):
        self.text = ""

    def __print(self, keluar=False):
        print (self.text)
        if keluar:
            Exit()

    def __input(self, text):
        try:
            return input(text)
        except:
            self.error("This function input not supported, please use python 3.7 or after")
            exit(0)

    def error(self, msg, isPrompt=False, isNewLine=False, keluar=False):
        if isNewLine:
            self.text += "\n"
        self.text += "[ " + self.timer.getTime() + " ] "
        self.text += "[KESALAHAN]: "
        self.text += msg
        if isPrompt:
            return self.__input(self.text)
        else:
            self.__print(keluar=keluar)
        self.reset()

    def warning(self, msg,  isPrompt=False, isNewLine=False):
        if isNewLine:
            self.text += "\n"
        self.text += "[ " + self.timer.getTime() + " ] "
        self.text += "[PERINGATAN]: "
        self.text += msg
        if isPrompt:
            return self.__input(self.text)
        else:
            self.__print()
        self.reset()

    def info(self, msg, isPrompt=False, isNewLine=False):
        if isNewLine:
            self.text += "\n"
        self.text += "[ " + self.timer.getTime() + " ] "
        self.text += "[INFORMASI]: "
        self.text += msg
        if isPrompt:
            return self.__input(self.text)
        else:
            self.__print()
        self.reset()