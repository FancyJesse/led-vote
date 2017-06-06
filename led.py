from threading import Lock
from time import sleep

import RPi.GPIO as GPIO

import config


LED_LIST = []


def setup():
	global LED_LIST
	GPIO.setmode(GPIO.BCM)
	for led_info in config.led_info:
		try:
			led = LED(led_info)
			LED_LIST.append(led)
		except:
			print('Failed to intitialize LED: {}'.format(led_info))


def cleanup():
	GPIO.cleanup()


def blink(led_id, delay=config.blink_delay):
	for led in LED_LIST:
		if led.id == led_id:
			led.blink(delay)
			return True
	return False


class LED:
	def __init__(self, led_info):
		self.pin = led_info[0]
		self.id = led_info[1]
		self.mutex = Lock()
		GPIO.setup(self.pin, GPIO.OUT)
	def on(self):
		GPIO.output(self.pin, True)
	def off(self):
		GPIO.output(self.pin, False)
	def blink(self, delay=config.blink_delay):
		self.mutex.acquire()
		self.on()
		sleep(delay)
		self.off()
		sleep(delay)
		self.mutex.release()


if __name__ == '__main__':
	try:
		print('START led.py')
		setup()
		print('\tLEDs Active:')
		for led in LED_LIST:
			print('\t\t{:2} - {}'.format(led.pin, led.id))
			led.blink()
	finally:	
		cleanup()
		print('END led.py')
