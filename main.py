import time

from machine import Pin  # type: ignore


def blink_led():
    pin_led = Pin(2, Pin.OUT)
    while True:
        pin_led.on()
        time.sleep(1)
        pin_led.off()
        time.sleep(1)


if __name__ == "__main__":
    blink_led()
