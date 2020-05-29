import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
#import serial
from neopixel import *

# 네오픽셀 LED 출력을 위한 설정
LED_COUNT		= 72	# 사용할 LED 개수 설정
LED_PIN			= 18	# 사용할 디지털 핀 설정
LED_FREQ_HZ		= 800000	# LED 신호의 주기 설정
LED_DMA			= 10	# 신호를 생성하기위한 DMA 채널 설정
LED_BRIGHTNESS	= 155	# LED 밝기 초기화
LED_INVERT		= False	# 신호 변환 사용시 True
LED_CHANNEL		= 0		# GPIO 13, 19, 41, 45, 53번 핀을 사용할 경우 '1'

# 네오픽셀 객체 초기화
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

# 아두이노로 보낼 시리얼 신호 초기화
#ser = serial.Serial("/dev/ttyUSB0", 9600)
u = "u"
u = u.encode('utf-8')
d = "d"
d = d.encode('utf-8')

# 파이어베이스 객체 초기화
cred = credentials.Certificate('mykey2.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://eseproject-bf8fe.firebaseio.com/'
})

# 데이터베이스 기본값 초기화
oldSpecial = "PowerOFF"
oldColor = "0"
oldBright = "0"
oldUV= "PowerOFF"

# 파도타기 세로
def waveMode1(special):
	print("waveMode1")
	j = 0
	while(special == db.reference('99-1=0/MoodLight/MusicMode/power').get()):
		c = db.reference('99-1=0/MoodLight/RGBValue').get()
		if c == "0":
			r, g, b = 0, 0, 0
		else:
			r = int(c[1] + c[2], 16)
			g = int(c[3] + c[4], 16)
			b = int(c[5] + c[6], 16)
		for i in range(12):
			strip.setPixelColor(i+j, Color(g, r, b))
		strip.show()
		j += 12
		if j > 61:
			while(j > 0):
				for i in range(12):
					strip.setPixelColor(i+j, Color(0, 0, 0))
				strip.show()
				j -=12
				time.sleep(0.2)

# 파도타기 가로
def waveMode2(special):
	print("waveMode2")
	while(special == db.reference('99-1=0/MoodLight/MusicMode/power').get()):
		c = db.reference('99-1=0/MoodLight/RGBValue').get()
		if c == "0":
			r, g, b = 0, 0, 0
		else:
			r = int(c[1] + c[2], 16)
			g = int(c[3] + c[4], 16)
			b = int(c[5] + c[6], 16)
		for i in range(12):
			for j in range(6):
				strip.setPixelColor(i+j*12, Color(g, r, b))
			strip.show()
			time.sleep(0.05)
		time.sleep(0.5)
		colorChange(strip, Color(0, 0, 0))
		for i in range(6):
			strip.setPixelColor(i*12, Color(g, r, b))
		strip.show()

# 같은 색 무지개
def rainbowMode1(special):
	print("waveMode1")
	j = 0
	while(special == db.reference('99-1=0/MoodLight/MusicMode/power').get()):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
			j += 1
		strip.show()
		time.sleep(20/1000.0)
	print("out")

# 다른 색 무지개
def rainbowMode2(special):
	print("rainbowMode2")
	j = 0
	while(special == db.reference('99-1=0/MoodLight/MusicMode/power').get()):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
			j += 1
		strip.show()
		time.sleep(20/1000.0)
	print("out")

# 무드등 동작
def moodLight(c, bright):
	if c == "0":
		colorChange(strip, Color(0, 0, 0))
	else:
		r = int(c[1] + c[2], 16)
		g = int(c[3] + c[4], 16)
		b = int(c[5] + c[6], 16)
		strip.setBrightness(bright)
		colorChange(strip, Color(g, r, b))

# UV LED 동작
def uvLed(uv):
	if uv == "PowerON":
		print("turn on uv led")
		#ser.write(y)
	else:
		print("turn off uv led")
        #ser.write(n)

# 네오픽셀 색 변경
def colorChange(strip, color):
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
	strip.show()

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

# 데이터 베이스 값 읽기
while(1):
	newSpecial = db.reference('99-1=0/MoodLight/MusicMode/power').get()
	newBright = db.reference('99-1=0/MoodLight/bright').get()
	newColor = db.reference('99-1=0/MoodLight/RGBValue').get()
	newMood = db.reference('99-1=0/MoodLight/power').get()
	newUV = db.reference('99-1=0/UVLED/power').get()
	
	# 기존 데이터베이스 값과 새로 가져온 데이터 베이스 값이 다를 경우 동작
	
	if oldSpecial != newSpecial:
		if newSpecial == "wave1":
			waveMode1(newSpecial)
		if newSpecial == "wave2":
			waveMode2(newSpecial)
		if newSpecial == "rainbow1":
			rainbowMode1(newSpecial)
		if newSpecial == "rainbow2":
			rainbowMode2(newSpecial)
		else:
			colorChange(strip, Color(0, 0, 0))
		oldSpecial = newSpecial        
	
	if oldColor != newColor:
		if newMood == "PowerON":
			moodLight(newColor, int(newBright))
			oldColor = newColor

	if oldBright!= newBright:
		if newMood == "PowerON":
			moodLight(newColor, int(newBright))
			oldBright = newBright

	if newMood == "PowerOFF":
		colorChange(strip, Color(0, 0, 0))
		#oldColor = '0'
		oldBright = '0'

	if oldUV != newUV:
		uvLed(newUV)
		oldUV = newUV

	print("running")
