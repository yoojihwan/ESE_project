import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
#import serial
from neopixel import *
import argparse

LED_COUNT		= 72
LED_PIN			= 18
LED_FREQ_HZ		= 800000
LED_DMA			= 10
LED_BRIGHTNESS	= 255
LED_INVERT		= False
LED_CHANNEL		= 0

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
args = parser.parse_args()
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

#ser = serial.Serial("/dev/ttyUSB0", 9600)
y = "y"
y = y.encode('utf-8')
n = "n"
n = n.encode('utf-8')

cred = credentials.Certificate('mykey2.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://eseproject-bf8fe.firebaseio.com/'
})

old_mm = "PowerOFF"
#old_b = "0"
old_c = "0"
old_mp = "PowerOFF"
old_uv = "PowerOFF"
#start = 0

def music_mode(new):
	if new == "PowerON":
		print("music mode on")
	else:
		print("music mode off")

#def brightness(new):
#	print("brightness =", new)

def color(new):
	print("color =", new)
	if new != "0":
		r = int("0x" + new[3] + new[4])
		g = int("0x" + new[1] + new[2])
		b = int("0x" + new[5] + new[6])
		colorChange(strip, Color(g, r, b))	

def MoodLight_on(new):
	if new == "PowerON":
		print("MoodLight on")
	else:
		print("MoodLight off")

def uvled(uv, t):
	if uv == "PowerON":
		print("turn on uv led")
		#ser.write(y)
#		return time.time()
	else:
		print("turn off uv led")
                #ser.write(n)
#		return 0

#def timer(t):
#	return{'1시간': 1, '2시간': 2, '3시간': 3, '4시간': 4, '5시간': 5, \
#'6시간': 6, '9시간': 9, '12시간': 12}.get(t, 0)

def colorChange(strip, color):
	for i in range(strip, numPixels()):
		strip.setPixelColor(i, color)
	strip.show()

while(1):
	new_mm = db.reference('99-1=0/MoodLight/MusicMode/power').get()
#	new_b = db.reference('99-1=0/MoodLight/bright').get()
	new_c = db.reference('99-1=0/MoodLight/RGBValue').get()
	new_mp = db.reference('99-1=0/MoodLight/power').get()
	new_uv = db.reference('99-1=0/UVLED/power').get()
#	new_t = db.reference('99-1=0/UVLED/timer').get()

	if old_mm != new_mm:
		music_mode(new_mm)
		old_mm = new_mm        
  
#	if old_b != new_b:
#		brightness(new_b)
#		old_b = new_b

	if old_c != new_c:
		color(new_c)
		old_c = new_c

	if old_mp != new_mp:
		MoodLight_on(new_mp)
		old_mp = new_mp

	if old_uv != new_uv:
#		old_t = timer(new_t)
#		if new_uv == "PowerON" and old_t == 0:
#			print("timer is 0")
#			ref = db.reference('99-1=0/UVLED')
#			ref.update({'power' : 'PowerOFF'})
#		else:
		start =uvled(new_uv, old_t)
		old_uv = new_uv

	print("running")

#	if start > 0:
#		if time.time() - start > old_t*3.0:
#			ref = db.reference('99-1=0/UVLED')
#			ref.update({'power' : 'PowerOFF'})
#	print(int(start))
