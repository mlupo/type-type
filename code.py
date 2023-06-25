from board import A3, A2, A1, A0, SCK, MISO, MOSI, D10, D5, D6, D3, BUTTON
import time
import digitalio
from adafruit_debouncer import Button

# user button
button = digitalio.DigitalInOut(BUTTON)
button.switch_to_input(pull=digitalio.Pull.UP)
switch = Button(button, long_duration_ms=500)

# BUSY high informs host that printer is busy and should wait before next data
BUSY = digitalio.DigitalInOut(D6)
BUSY.direction = digitalio.Direction.INPUT
BUSY.pull = digitalio.Pull.DOWN

# SEL To Host - A high value indicates that a printer is present
SEL = digitalio.DigitalInOut(D3)
SEL.direction = digitalio.Direction.INPUT
SEL.pull = digitalio.Pull.DOWN

# STROBE - To Printer, low pulse indicates that there’s valid data on D[7:0]
STROBE = digitalio.DigitalInOut(D5)
STROBE.direction = digitalio.Direction.OUTPUT
STROBE.value = 1

# high/low values on these pins indicate the binary data being sent
board_pin_list = [A3, A2, A1, A0, SCK, MISO, MOSI, D10]
# DB25 pin num:   p9  p8  p7  p6  p5   p4    p3    p2

# initialize pins as digitalio objects
for num, pin in enumerate(board_pin_list.copy()):
    board_pin_list[num] = digitalio.DigitalInOut(pin)
    board_pin_list[num].direction = digitalio.Direction.OUTPUT
    board_pin_list[num].value = 0


def resetPins(pins):
    for pin in pins:
        pin.value = 0


def sendChar(char, wait=1):
    data = [bin(binary) for binary in bytearray(char)]
    printable_data = data[0].replace('b', '')
    while len(printable_data) < 8:
        printable_data = "0" + printable_data
    for binary_val, pinval in zip(printable_data, board_pin_list):
        pinval.value = int(binary_val)
    print("char:", char, "-", "binary data ready:", printable_data)
    time.sleep(0.0005*wait)
    print("strobe start")
    STROBE.value = False
    time.sleep(0.001*wait)
    STROBE.value = True
    print("strobe end\n")
    time.sleep(0.0005*wait)
    resetPins(board_pin_list)


def sendText(text, busy_signal, sel_signal, extra_beeps=False, beep_count=5):
    count = len(text)-1
    position = 0
    time.sleep(0.005)
    while position <= count:
        if not busy_signal.value:
            time.sleep(0.0005)
            sendChar(text[position])
            position += 1
            if extra_beeps and not (position % beep_count):
                sendChar("\a")  # ASCII Bell (BEL)
                print("beep!")
        if not sel_signal.value:
            print("bye!")
            break


story = "not a story...yet!\n\n\n"
while True:
    switch.update()
    if SEL.value and switch.fell:
        try:
            with open('2_MERCEDES.txt', 'r') as reader:
                story = reader.read()
            sendText(story, busy_signal=BUSY, sel_signal=SEL)
        except OSError:
            sendText("no file found", busy_signal=BUSY, sel_signal=SEL)
            print("file not found, try again?")
