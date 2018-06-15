import Adafruit_CharLCD as LCD

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

class LCD:
    def __init__(self):
        self.lcd = LCD.Adafruit_CharLCDBackpack()

    def getInstance(self):
        return self.lcd

    def getRows(self):
        return lcd_rows

    def getColumns(self):
        return lcd_columns
