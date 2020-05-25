import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
from color_change import color_change
#import bord
#import neopixel
#import neo
import serial

#ser = serial.Serial("/dev/ttyUSB0", 9600)
y = "y"
y = y.encode('utf-8')
n = "n"
n = n.encode('utf-8')

#pixels = neopixel.NeoPixel(board.D18, 72)

cred = credentials.Certificate('mykey2.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://eseproject-bf8fe.firebaseio.com/'
})

old_mm = "PowerOFF"
old_b = "0"
old_c = "0"
old_mp = "PowerOFF"
old_uv = "PowerOFF"
start = 0

def music_mode(new):
	if new == "PowerON":
		print("music mode on")
	else:
		print("music mode off")

def brightness(new):
	print("brightness =", new)

def color(new):
	print("color =", new)
    #print(color_change(new))

def MoodLight_on(new):
	if new == "PowerON":
		print("MoodLight on")
	else:
		print("MoodLight off")

def uvled(uv, t):
	if uv == "PowerON":
		print("turn on uv led")
		#ser.write(y)
		return time.time()
	else:
		print("turn off uv led")
       #ser.write(n)
		return 0

def timer(t):
	return{'1시간': 1, '2시간': 2, '3시간': 3, '4시간': 4, '5시간': 5, \
'6시간': 6, '9시간': 9, '12시간': 12}.get(t, 0)

while(1):
	new_mm = db.reference('99-1=0/MoodLight/MusicMode/power').get()
	new_b = db.reference('99-1=0/MoodLight/bright').get()
	new_c = db.reference('99-1=0/MoodLight/RGBValue').get()
	new_mp = db.reference('99-1=0/MoodLight/power').get()
	new_uv = db.reference('99-1=0/UVLED/power').get()
	new_t = db.reference('99-1=0/UVLED/timer').get()

	if old_mm != new_mm:
		music_mode(new_mm)
		old_mm = new_mm        
  
	if old_b != new_b:
		brightness(new_b)
		old_b = new_b

	if old_c != new_c:
		color(new_c)
		old_c = new_c

	if old_mp != new_mp:
		MoodLight_on(new_mp)
		old_mp = new_mp

	if old_uv != new_uv:
		old_t = timer(new_t)
		if new_uv == "PowerON" and old_t == 0:
			print("timer is 0")
			ref = db.reference('99-1=0/UVLED')
			ref.update({'power' : 'PowerOFF'})
		else:
			start =uvled(new_uv, old_t)
			old_uv = new_uv

	if start > 0:
		if time.time() - start > old_t*3.0:
			ref = db.reference('99-1=0/UVLED')
			ref.update({'power' : 'PowerOFF'})
	print(int(start))
