import RPi.GPIO as GPIO
from time import sleep
import sys
from ultraModule import getDistance
from TurnModule import *
from go_any import *


# =======================================================================
#  set GPIO warnings as false
# =======================================================================
GPIO.setwarnings(False)

# =======================================================================
# set up GPIO mode as BOARD
# =======================================================================
GPIO.setmode(GPIO.BOARD)

leftmostled=16
leftlessled=18
centerled=22
rightlessled=40
rightmostled=32

GPIO.setup(leftmostled, GPIO.IN)
GPIO.setup(leftlessled, GPIO.IN)
GPIO.setup(centerled,   GPIO.IN)
GPIO.setup(rightmostled, GPIO.IN) #
GPIO.setup(rightlessled, GPIO.IN) #

def trackingModule():
	reli = []
	reli.append(GPIO.input(leftmostled))
	reli.append(GPIO.input(leftlessled))
	reli.append(GPIO.input(centerled))
	reli.append(GPIO.input(rightlessled))
	reli.append(GPIO.input(rightmostled))
	return reli

def mover(reli, speed):
	speed = speed
	if reli == [0,0,1,1,1] or reli == [0,1,1,1,1] or reli == [0,0,0,1,1] or reli == [0,0,0,0,1]:
		leftSwingTurn(speed,0.5)
	if reli == [1,0,0,0,1] or reli == [1,1,0,1,1] or reli == [1,1,1,1,1]:
		go_forward(speed, 0.5)
	if reli == [1,1,0,0,0] or reli == [1,1,1,1,0] or reli == [1,1,1,0,0] or reli == [1,0,0,0,0]:
		rightSwingTurn(speed, 0.5)
	else:
		go_forward(speed, 0.5)

def avoider():
	leftSwingTurn(20,2)
	go_forward(20,2)
	rightSwingTurn(20,2)

GPIO.setwarnings(False)
pwm_setup()

mindis = 30
obstacle = 1

SwingPr = 90
SwingTr = 0.5

if __name__ == "__main__":
	while True:
		try:
			if getDistance() < mindis:
				avoider()
			else:
				mover(trackingModule(), 20)
		except KeyboardInterrupt:
			GPIO.cleanup()
			pwm_low()
