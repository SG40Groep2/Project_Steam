import RPi.GPIO as GPIO
import time


GPIO.setwarnings(0)

sr04_trig = 21
sr04_echo = 20
servo = 25
pieper = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(sr04_trig, GPIO.OUT)
GPIO.setup(sr04_echo, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(servo, GPIO.OUT)
GPIO.setup(pieper, GPIO.OUT)


def sr04(trig_pin, echo_pin, pieper):
    while True:
        GPIO.output(trig_pin, True)
        time.sleep(0.000001)
        GPIO.output(trig_pin, False)

        begintijd = time.time()
        stoptijd = time.time()

        while GPIO.input(echo_pin) == 0:
            begintijd = time.time()
        while GPIO.input(echo_pin) == 1:
            stoptijd = time.time()

        totale_tijd = stoptijd - begintijd
        afstand = totale_tijd // 0.000058

        servo_pulse(servo, afstand)
        pieper_functie(pieper, afstand)
        time.sleep(0.5)

def servo_pulse(pin_nr, afstand):
    afstand = afstand - 20
    var = afstand / 10
    var = var + 2
    if var >= 100:
        var = 99.999999
    pwm_servo = GPIO.PWM(pin_nr, 50)
    pwm_servo.start(var)
    time.sleep(0.02)


def pieper_functie(pieper, afstand):
    if afstand < 30:
        print('Pieper gaat af')
        GPIO.output(pieper, 0)
    else:
        GPIO.output(pieper, 1)

