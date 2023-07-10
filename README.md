# type-type
This project uses an Adafruit KB2040 board to send parallel data to an electronic typewriter via its Centronics port.

## What is Happening Here?
The KB2040 has at its heart the Raspberry Pi RP2040 chip, running CircuitPython. The program ingests a text file, and sends the data character by character until it reaches a newline, at which point the typewriter sends a busy signal, and taps out its text buffer. Once the typewriter is no longer "busy" the code sends more characters, repeating the process until the file is completely printed. The KB2040 is wired directly to a DB-25 connector which in turn connects to a DB-25 to Centronics cable in order to send data back and forth.

## Wait, But How?
Thank goodness the parallel printer port is clearly defined, and it is (reasonably!) easy to mess around with! With a lot of help from an interesting writeup on [making a fake parallel printer](https://tomverbeure.github.io/2023/01/24/Fake-Parallel-Printer-Capture-Tool-HW.html) by [@tomverbeure](https://github.com/tomverbeure), I was able to get a sense of the necessary pins and timings required to send parallel data. This project uses the KB2040 to set high values on a series of pins connected to the parallel ports data pins, as well as the port's "STROBE" pin. During every STROBE cycle, the high/low pins are interpreted by the typewriter as a binary character, which it prints after receiving a newline, or certain other escape characters.
