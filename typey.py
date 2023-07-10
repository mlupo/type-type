# typey
from time import sleep


class TypeManager:
    """class to manage data to and from printer"""

    def __init__(self, pins, busy_signal, sel_signal, strobe_signal, button):
        self.pins = pins
        self.busy_signal = busy_signal
        self.sel_signal = sel_signal
        self.strobe_signal = strobe_signal
        self.button = button

    def resetPins(self):
        for pin in self.pins:
            pin.value = 0

    def sendChar(self, char, wait=1):
        data = [bin(binary) for binary in bytearray(char)]
        binary_data = data[0].replace('b', '')
        # reverse the binary data to match D[7:0] alignment of pins list
        for bin_val, pin_val in zip(reversed(binary_data), self.pins):
            pin_val.value = int(bin_val)
        # print("char:", char, "-", "binary data ready:", binary_data)
        sleep(0.0005*wait)
        # print("strobe start")
        self.strobe_signal.value = False
        sleep(0.0005*wait)
        self.strobe_signal.value = True
        # print("strobe end\n")
        sleep(0.0005*wait)
        self.resetPins()

    def sendText(self, text, extra_beeps=False, beep_count=5):
        count = len(text)
        position = 0
        sleep(0.005)
        while position < count:
            self.button.update()
            if not self.busy_signal.value:
                sleep(0.0005)
                self.sendChar(text[position])
                position += 1
                if extra_beeps and (position % beep_count) == 0:
                    self.sendChar("\a")  # ASCII Bell (BEL)
                    print("beep!")
            if not self.sel_signal.value or self.button.long_press:
                print("bye!")
                break
