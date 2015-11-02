import time

import multiprocessing
from multiprocessing import Process, Event

import mraa


class RGBLEDProcess(Process):

    def __init__(self, red, green, blue, strobe, sleep=0.5, name='RGBLEDProcess'):
        Process.__init__(self, name=name)
        self.logger = multiprocessing.get_logger()
        self.event = Event()
        self.red = red
        self.green = green
        self.blue = blue
        self.sleep = sleep
        self.strobe = strobe
        self.blue_gpio = 0
        self.green_gpio = 1
        self.red_gpio = 2

    def _led_on(self):
        self.logger.debug('LED on')
        self.red_pwm.write(self.red)
        self.green_pwm.write(self.green)
        self.blue_pwm.write(self.blue)

    def _led_off(self):
        self.logger.debug('LED off')
        self.red_pwm.write(0)
        self.green_pwm.write(0)
        self.blue_pwm.write(0)

    def run(self):
        self.event.set()
        self.logger.debug('PID: %d' % multiprocessing.current_process().pid)

        self.red_pwm = mraa.Pwm(self.red_pgio)
        self.green_pwm = mraa.Pwm(self.green_pgio)
        self.blue_pwm = mraa.Pwm(self.blue_pgio)
        self.red_pwm.period_us(700)
        self.green_pwm.period_us(700)
        self.blue_pwm.period_us(700)
        self.red_pwm.enable(True)
        self.green_pwm.enable(True)
        self.blue_pwm.enable(True)

        while self.event.is_set():
            self._led_on()
            time.sleep(self.sleep)
            if self.strobe:
                self._led_off()
                time.sleep(self.sleep)

    def stop(self):
        self.logger.debug('Process will halt.')
        self.event.clear()
        self._led_off()
        self.terminate()