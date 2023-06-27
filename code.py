from board import A3, A2, A1, A0, SCK, MISO, MOSI, D10, D5, D6, D3, BUTTON
from digitalio import DigitalInOut, Direction, Pull
from adafruit_debouncer import Button
from typey import TypeManager

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
# list is organized bit 7:0 so that short binary chars like '01010' slot easily
# into the for loop in sendChar()

# initialize pins as digitalio objects
for num, pin in enumerate(board_pin_list.copy()):
    board_pin_list[num] = DigitalInOut(pin)
    board_pin_list[num].direction = Direction.OUTPUT
    board_pin_list[num].value = 0

typeWriter = TypeManager(board_pin_list, BUSY, SEL, STROBE)

story = "not a story...yet!\n\n\n"
folder = "/stories/"
while True:
    # print("hey")
    switch.update()
    if SEL.value and switch.fell:
        try:
            with open(folder+'2_MERCEDES.txt', 'r') as reader:
                story = reader.read()
            typeWriter.sendText(story)
        except OSError:
            typeWriter.sendText("no file found\n\n\n\n")
            print("file not found, try again?")
