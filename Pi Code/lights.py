import time
import RPi.GPIO as gp


def strobe(times=10):
    while times:
        gp.output(18, True)
        time.sleep(1)
        gp.output(18, False)
        time.sleep(1)
    times -= 1
