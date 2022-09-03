# coding=utf-8

import time
import RPi.GPIO as GPIO

gpio_initialized = False


class Abstract_MusicalInstrument:
    id = -1
    name = ''
    description = ''

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description
        pass

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def play(self, hertz, duration_seconds):
        print("You have to override the Abstract_MusicalInstrument::play().")
        assert False
        pass


class Abstract_Stepper(Abstract_MusicalInstrument):
    io_a1 = None
    io_a2 = None
    io_b1 = None
    io_b2 = None

    # list_gpio: board number of gpio
    def __init__(self, id, name, descript, io_a1, io_a2, io_b1, io_b2):
        Abstract_MusicalInstrument.__init__(self, id, name, descript)
        init_gpio()
        self.io_a1 = io_a1
        self.io_a2 = io_a2
        self.io_b1 = io_b1
        self.io_b2 = io_b2

        GPIO.setup(self.io_a1, GPIO.OUT)
        GPIO.setup(self.io_a2, GPIO.OUT)
        GPIO.setup(self.io_b1, GPIO.OUT)
        GPIO.setup(self.io_b2, GPIO.OUT)
        # GPIO.setup(38, GPIO.OUT)
        # GPIO.setup(40, GPIO.OUT)

        GPIO.output(self.io_a1, 0)
        GPIO.output(self.io_a2, 0)
        GPIO.output(self.io_b1, 0)
        GPIO.output(self.io_b2, 0)
        # GPIO.output(38, 1)
        # GPIO.output(40, 1)
        pass

    def _step(self, w1, w2, w3, w4):
        GPIO.output(self.io_a1, w1)
        GPIO.output(self.io_a2, w2)
        GPIO.output(self.io_b1, w3)
        GPIO.output(self.io_b2, w4)

    # 单、双六拍运行
    # def _forward(self, delay):
    #     # 调用一次产生两次震动
    #     self._step(1, 0, 0, 0)
    #     time.sleep(delay)
    #     self._step(1, 0, 1, 0)
    #     time.sleep(delay)
    #     self._step(0, 0, 1, 0)
    #     time.sleep(delay)
    #     self._step(0, 1, 1, 0)
    #     time.sleep(delay)
    #
    #     self._step(0, 1, 0, 0)
    #     time.sleep(delay)
    #     self._step(0, 1, 0, 1)
    #     time.sleep(delay)
    #     self._step(0, 0, 0, 1)
    #     time.sleep(delay)
    #     self._step(1, 0, 0, 1)
    #     time.sleep(delay)

    # 双三拍运行
    def _forward(self, delay):
        self._step(1, 0, 1, 0)
        time.sleep(delay)
        self._step(0, 1, 1, 0)
        time.sleep(delay)

        self._step(0, 1, 0, 1)
        time.sleep(delay)
        self._step(1, 0, 0, 1)
        time.sleep(delay)

    def get_delay(self, hertz):
        print("You have to override the Abstract_Stepper::get_delay().")
        assert False

    def play(self, hertz, duration_seconds):
        delay = self.get_delay(hertz)
        begin_time = time.time()
        # print("_forward(%f)" % delay)
        while (time.time()-begin_time) <= duration_seconds:
            self._forward(delay)
        pass


def init_gpio():
    global gpio_initialized
    if gpio_initialized:
        return
    GPIO.setmode(GPIO.BOARD)  # 设置引脚的编码方式
    GPIO.setwarnings(False)
    gpio_initialized = True
