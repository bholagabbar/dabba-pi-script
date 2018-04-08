import time
import RPi.GPIO as gp


def strobe(times=10, sec=1):
    while times:
        gp.output(18, True)
        time.sleep(sec)
        gp.output(18, False)
        time.sleep(sec)
    times -= 1
