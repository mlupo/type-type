from board import A3, A2, A1, A0, SCK, MISO, MOSI, D10, D5, D6, D3, BUTTON
from time import sleep
from digitalio import DigitalInOut, Direction, Pull
from adafruit_debouncer import Button

# user button
button = DigitalInOut(BUTTON)
button.switch_to_input(pull=Pull.UP)
switch = Button(button, long_duration_ms=500)

# BUSY high informs host that printer is busy and should wait before next data
BUSY = DigitalInOut(D6)
BUSY.direction = Direction.INPUT
BUSY.pull = Pull.DOWN

# SEL To Host - A high value indicates that a printer is present
SEL = DigitalInOut(D3)
SEL.direction = Direction.INPUT
SEL.pull = Pull.DOWN

# STROBE - To Printer, low pulse indicates that there’s valid data on D[7:0]
STROBE = DigitalInOut(D5)
STROBE.direction = Direction.OUTPUT
STROBE.value = 1

# high/low values on these pins indicate the binary data being sent
# DB25 pin num:   p2    p3    p4    p5  p6  p7  p8  p9
board_pin_list = [D10, MOSI, MISO, SCK, A0, A1, A2, A3]
# binary data bit: 7    6      5    4    3   2   1   0
# list is bit 7:0 so that binary chars like '01010' slot easily into sendChar()

# initialize pins as digitalio objects
for num, pin in enumerate(board_pin_list.copy()):
    board_pin_list[num] = DigitalInOut(pin)
    board_pin_list[num].direction = Direction.OUTPUT
    board_pin_list[num].value = 0


def resetPins(pins):
    for pin in pins:
        pin.value = 0


def sendChar(char, pins, wait=1):
    data = [bin(binary) for binary in bytearray(char)]
    binary_data = data[0].replace('b', '')
    # we reverse the binary data so that 4bit characters load the correct pins
    for bin_val, pin_val in zip(reversed(binary_data), pins):
        pin_val.value = int(bin_val)
    print("char:", char, "-", "binary data ready:", binary_data)
    sleep(0.0005*wait)
    print("strobe start")
    STROBE.value = False
    sleep(0.001*wait)
    STROBE.value = True
    print("strobe end\n")
    sleep(0.0005*wait)
    resetPins(pins)


def sendText(text, busy_signal, sel_signal, extra_beeps=False, beep_count=5):
    count = len(text)-1
    position = 0
    sleep(0.005)
    while position <= count:
        if not busy_signal.value:
            sleep(0.0005)
            sendChar(text[position], pins=board_pin_list)
            position += 1
            if extra_beeps and (position % beep_count) == 0:
                sendChar("\a")  # ASCII Bell (BEL)
                print("beep!")
        if not sel_signal.value:
            print("bye!")
            break


story = "not a story...yet!\n\n\n"
folder = "/stories/"
while True:
    # print("hey")
    switch.update()
    if SEL.value and switch.fell:
        try:
            with open(folder+'2_MERCEDES.txt', 'r') as reader:
                story = reader.read()
            sendText(story, busy_signal=BUSY, sel_signal=SEL)
        except OSError:
            sendText("no file found\n\n\n\n", busy_signal=BUSY, sel_signal=SEL)
            print("file not found, try again?")
