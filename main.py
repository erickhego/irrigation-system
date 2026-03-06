import time

import ntptime  # type: ignore
from machine import ADC, Pin  # type: ignore

MAX = 65535
MIN = 34000
D0 = Pin(0, Pin.OUT)

ntptime.settime()


def humidity_sensor():
    adc = ADC(0)
    D0.on()

    lectures_range = MAX - MIN
    lecture = adc.read_u16()
    percentage = ((MAX - lecture) / lectures_range) * 100
    D0.off()

    return (lecture, 100 if percentage > 100 else percentage)


if __name__ == "__main__":
    D0.off()
    time.sleep(10)
    print("Iniciando lectura")
    while True:
        humidity, h_percentage = humidity_sensor()
        date_time = time.localtime(time.time() + (-6 * 3600))
        date_time_stamp = f"{date_time[0]}-{date_time[1]:02d}-{date_time[2]:02d} {date_time[3]:02d}:{date_time[4]:02d}:{date_time[5]:02d}"
        print(
            f"datetime: {date_time_stamp} Lectura: {humidity} - porcetaje: {h_percentage}"
        )
        # Aqui irá el POST a la API
        time.sleep(5)
