import RPi.GPIO as GPIO

GPIO.setwarnings(0)

clock_pin = 19
data_pin = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(clock_pin, GPIO.OUT)
GPIO.setup(data_pin, GPIO.OUT)


def apa102_send_bytes(clock_pin, data_pin, bytes):
    for byte in bytes:
        for bit in byte:
            if bit == '1':
                GPIO.output(data_pin, 1)
            else:
                GPIO.output(data_pin, 0)
            GPIO.output(clock_pin, 1)
            GPIO.output(clock_pin, 0)


def apa102(clock_pin, data_pin, colors):
    nullen_bytes = [[], [], [], []]
    for x in range(4):
        for i in range(8):
            nullen_bytes.append(str(0))
    apa102_send_bytes(clock_pin, data_pin, nullen_bytes)

    ledjes = [[], [], [], []]
    for x in range(8):
        ledjes[0] = str(format(195, '08b'))
        for i in range(3):
            ledjes[i + 1] = str(format(colors[x][i], '08b'))
        apa102_send_bytes(clock_pin, data_pin, ledjes)

    een_bytes = [[], [], [], []]
    for x in range(4):
        for i in range(8):
            een_bytes.append(str(1))
    apa102_send_bytes(clock_pin, data_pin, een_bytes)


def neopixels(aantal):
    red = [0, 0, 255]
    green = [0, 255, 0]
    knipperen = [[], [], [], [], [], [], [], []]
    for x in range(aantal):
        knipperen[7 - x] = green
    for x in range(8 - aantal):
        knipperen[x] = red

    apa102(clock_pin, data_pin, knipperen)
