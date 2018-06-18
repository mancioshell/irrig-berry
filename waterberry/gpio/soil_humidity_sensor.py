from waterberry.utils.logger import logger
from waterberry.gpio.board import Board

class SoilHumiditySensor:
    def __init__(self, pin_di, pin_do, pin_clk, pin_cs):
        self.pin_di = gpio_dao.getPinByName(pin_di)
        self.pin_do = gpio_dao.getPinByName(pin_do)
        self.pin_clk = gpio_dao.getPinByName(pin_clk)
        self.pin_cs = gpio_dao.getPinByName(pin_cs)

    def getADC(self, channel):
        board = Board()
        board.initBoard()

        # 1. CS LOW.
        board.disablePin(self.pin_cs) # clear last transmission
        board.enablePin(self.pin_cs) # bring CS low

        # 2. Start clock
        board.enablePin(self.pin_clk) # start clock low

        # 3. Input MUX address
        for i in [1,1,channel]: # start bit + mux assignment
            if (i == 1):
                board.disablePin(self.pin_di)
            else:
                board.enablePin(self.pin_di)

                board.disablePin(self.pin_clk)
                board.enablePin(self.pin_clk)

        # 4. read 8 ADC bits
        ad = 0
        for i in range(8):
            board.disablePin(self.pin_clk)
            board.enablePin(self.pin_clk)
            ad <<= 1 # shift bit
            if (board.getPinState(self.pin_do)):
                ad |= 0x1 # set first bit

        # 5. reset
        board.disablePin(self.pin_cs)

        return ad
