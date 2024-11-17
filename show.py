from ssd1306 import SSD1306_I2C
from machine import I2C, Pin

class WDT_NOP:
    def feed(self):
        return

class DummyOLED:
    def text(self, _, __, ___):
        return

    def fill(self, _):
        return

    def show(self):
        return

    def poweron(self):
        return

    def poweroff(self):
        return

class Show:

    def __init__(self, wdt = WDT_NOP()):
        oled_i2c = I2C(1, sda=Pin(21), scl=Pin(22), freq=200000)
        self.lines = []
        try:
            self.oled = SSD1306_I2C(128, 64, oled_i2c)
        except:
            print('Failed to initialize screen')
            self.oled = DummyOLED()
        self.wdt = wdt

    def line(self, text):
        self.wdt.feed()
        print(text)
        if len(self.lines) > 3:
            self.lines = []
        self.lines.append(text)
        try:
            self.oled.fill(0)
            offset = 0
            for index, line in enumerate(self.lines):
                if index == 1:
                    offset += 6
                self.oled.text(line, 0, offset)
                offset += 12
            self.oled.show()
        except Exception as err:
            print(f'failed to show line: {text}\n {err}')

    def dict(self, dict):
        self.lines = []
        for k, v in dict.items():
            self.line(f"{k}: {v}")

    def display_on(self):
        print('Screen on')
        self.oled.poweron()

    def display_off(self):
        print('Screen off')
        self.oled.poweroff()