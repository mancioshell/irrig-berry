from waterberry.utils.logger import logger

class SoilHumiditySensor:
    def __init__(self, board, **kwargs):
        self.board = board
        self.pin_di = kwargs['pin_di']
        self.pin_do = kwargs['pin_do']
        self.pin_clk = kwargs['pin_clk']
        self.pin_cs = kwargs['pin_cs']

    def getADC(self, channel):
        self.board.initBoard()

        # 1. CS LOW.
        self.board.disablePin(self.pin_cs) # clear last transmission
        self.board.enablePin(self.pin_cs) # bring CS low

        # 2. Start clock
        self.board.enablePin(self.pin_clk) # start clock low

        # 3. Input MUX address
        for i in [1,1,channel]: # start bit + mux assignment
            if (i == 1):
                self.board.disablePin(self.pin_di)
            else:
                self.board.enablePin(self.pin_di)

                self.board.disablePin(self.pin_clk)
                self.board.enablePin(self.pin_clk)

        # 4. read 8 ADC bits
        ad = 0
        for i in range(8):
            self.board.disablePin(self.pin_clk)
            self.board.enablePin(self.pin_clk)
            ad <<= 1 # shift bit
            if (self.board.getPinState(self.pin_do)):
                ad |= 0x1 # set first bit

        # 5. reset
        self.board.disablePin(self.pin_cs)

        return ad

    def getData(self):
        channel_0 = self.getADC(0)
        channel_1 = self.getADC(1)
        return (channel_0+channel_1)/2
