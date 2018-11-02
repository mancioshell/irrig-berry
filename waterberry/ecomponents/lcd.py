import configparser
import os

from waterberry.utils.logger import logger

from waterberry.utils.definition import ROOT_DIR

file = os.path.join(ROOT_DIR, 'config/waterberry.config')
config = configparser.ConfigParser()
config.read_file(open(file))
raspberry = config.getboolean(os.environ['PLATFORM'], 'RPI_GPIO')
lcd = config.getboolean(os.environ['PLATFORM'], 'LCD')

if raspberry:
    import Adafruit_CharLCD as LCDRaspberry

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

class LCD:
    def __init__(self):
        if raspberry and lcd:
            self.lcd = LCDRaspberry.Adafruit_CharLCDBackpack()

    def writeData(self, humidity, temperature):
        if raspberry and lcd:
            self.lcd.set_backlight(0)
            self.lcd.clear()
            self.lcd.message("{}u'\u2103'\n{}%".format(temperature, humidity))
        else:
            print("Writing {}u'\u2103'\n{}%".format(temperature, humidity))
