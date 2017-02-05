from threading import Lock
from time import sleep

from logger import log
import RPi.GPIO as GPIO
import config


LED_LIST = []


def setup():
	global LED_CONNECTED, LED_LIST
	try:
		GPIO.setmode(GPIO.BCM)
		for led_info in config.LED_INFO:
			try:
				led = LED(led_info)
				LED_LIST.append(led)
			except Exception as e:
				raise Exception('{} - {} - {}'.format(__name__, led_info, e))
		log(__name__, 'LEDs Active: {}'.format(dict(map(lambda x: [x.id, x.pin], LED_LIST))))
	except Exception as e:
		raise Exception('{} - {}'.format(__name__, e))


def cleanup():
	GPIO.cleanup()
	log(__name__, 'GPIO Cleaned Up')


def blink(led_id):
	for led in LED_LIST:
		if led.id == led_id:
			led.blink()
			break

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
	def blink(self):
		self.mutex.acquire()
		self.on()
		sleep(config.LED_BLINK_DELAY)
		self.off()
		sleep(config.LED_BLINK_DELAY)
		self.mutex.release()
