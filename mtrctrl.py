from RPi import GPIO


class Controller:

    def __init__(self, gpio_port: int):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        self.is_on = False
        self.__em_channel = gpio_port

        print("setting up gpio controller on channel " + str(self.__em_channel))

        GPIO.setup(self.__em_channel, GPIO.OUT)

    def turn_on(self):
        print(f'turning on gpio channel {self.__em_channel}')
        GPIO.output(self.__em_channel, GPIO.HIGH)
        self.is_on = True

    def turn_off(self):
        print(f'turning off gpio channel {self.__em_channel}')
        GPIO.output(self.__em_channel, GPIO.LOW)
        self.is_on = False

    def cleanup(self):
        GPIO.cleanup()
        self.is_on = False
