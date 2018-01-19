def sound_sensor(time):
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
	# print dist
	return dist