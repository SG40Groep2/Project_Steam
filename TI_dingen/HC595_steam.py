import RPi.GPIO as GPIO
import time

GPIO.setwarnings( 0 )

shift_clock_pin = 5
latch_clock_pin = 6
data_pin = 13

GPIO.setmode( GPIO.BCM )
GPIO.setup( shift_clock_pin, GPIO.OUT )
GPIO.setup( latch_clock_pin, GPIO.OUT )
GPIO.setup( data_pin, GPIO.OUT )

def hc595(shift_clock_pin, latch_clock_pin, data_pin, value, delay):
    for x in range(0,8):
        if value %2 == 1:
            GPIO.output(data_pin, GPIO.HIGH)
        else:
            GPIO.output(data_pin, GPIO.LOW)
        GPIO.output(shift_clock_pin, GPIO.HIGH)
        GPIO.output(shift_clock_pin, GPIO.LOW)
        value = value // 2
    GPIO.output(latch_clock_pin, GPIO.HIGH)
    GPIO.output(latch_clock_pin, GPIO.LOW)
    time.sleep(delay)


def achievenentleds(achievenents):
        lamps_list = [1,2,4,8,16,32,64,128]
        while True:
            for x in range(0, achievenents):
                if lamps_list[x] == 1:
                    hc595(shift_clock_pin, latch_clock_pin, data_pin, lamps_list[x], 0)
                else:
                    hc595(shift_clock_pin, latch_clock_pin, data_pin, lamps_list[x], 0.00001)