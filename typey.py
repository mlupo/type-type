# typey
from time import sleep


class TypeManager:
    """class to manage data to and from printer"""

    def __init__(self, pins, busy_signal, sel_signal, strobe_signal, button):
        """requires a list of pins which map to the parallel data pins, as well
        as the sel signal from the typewriter. Strobe pulsed low sends data in
        the buffer. The button should be an adafruit_debouncer Button object"""
        self.pins = pins
        self.busy_signal = busy_signal
        self.sel_signal = sel_signal
        self.strobe_signal = strobe_signal
        self.button = button

    def resetPins(self):
        """set all pins to low"""
        for pin in self.pins:
            pin.value = 0

    def sendChar(self, char, wait=1):
        """first, take the single character string and get its binary
        representation"""
        data = [bin(binary) for binary in bytearray(char)]
        binary_data = data[0].replace('b', '')
        # reverse the binary data to match D[7:0] alignment of pins list
        for bin_val, pin_val in zip(reversed(binary_data), self.pins):
            pin_val.value = int(bin_val)
        # print("char:", char, "-", "binary data ready:", binary_data)
        sleep(0.0005*wait)
        # print("strobe start")
        self.strobe_signal.value = False  # strobe pulsed low sends the char
        sleep(0.0005*wait)
        self.strobe_signal.value = True
        # print("strobe end\n")
        sleep(0.0005*wait)
        self.resetPins()

    def sendText(self, text, extra_beeps=False, beep_count=5):
        """sendText takes in a string which could be a huge multi-line
        text file, or a single character. Note that the typewriter will not
        print any data until it receives an escape char (usually a newline).
        if extra_beeps is true, the printer will make its bell sound after
        the number of beep_count characters."""
        count = len(text)
        position = 0
        sleep(0.005)
        # position is tracked so that the while loop can "pause" during BUSY
        while position < count:
            self.button.update()
            if not self.sel_signal.value or self.button.long_press:
                """if the button is long pressed, or if the printer's "online"
                button is pressed, the loop breaks, and printing should stop"""
                print("bye!")
                break
            if not self.busy_signal.value:
                sleep(0.0005)
                self.sendChar(text[position])
                position += 1
                if extra_beeps and (position % beep_count) == 0:
                    self.sendChar("\a")  # ASCII Bell (BEL)
                    print("beep!")
