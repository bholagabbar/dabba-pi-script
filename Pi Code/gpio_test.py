import time

import RPi.GPIO as gp

gp.setmode(gp.BCM)
gp.setup(23, gp.OUT)
gp.setup(24, gp.IN)
gp.setwarnings(False)

while True:
	gp.output(23, True)
	time.sleep(0.00001)
	gp.output(23, False)

	while gp.input(24) == 0:
		pulseStart = time.time()

	while gp.input(24) == 1:
		pulseEnd = time.time()

	pulseDur = pulseEnd - pulseStart
	dist = pulseDur * 17150
	dist = round(dist, 2)
	print dist
