
class Controller:

    def __init__(self, gpio_port: int):
        self.is_on = False
        self.__em_channel = gpio_port
        print('server does not have RPi.GPIO installed, using test mtrctrl')

    def turn_on(self):
        print(f'turning on gpio channel {self.__em_channel}')
        self.is_on = True

    def turn_off(self):
        print(f'turning off gpio channel {self.__em_channel}')
        self.is_on = False

    def cleanup(self):
        self.is_on = False
