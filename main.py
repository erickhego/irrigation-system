import time

import ntptime  # type: ignore
import requests  # type: ignore
from machine import ADC, Pin  # type: ignore

from config import SENSOR_CREATE_URL, SENSOR_LECTURE_URL  # type: ignore

ntptime.settime()

MAX: int = 65_535
MIN: int = 34_000
D0: Pin = Pin(0, Pin.OUT)
SENSOR_ID: int = 1
SENSOR_NAME: str = "Lengua de suegra"
SENSOR_DESCRIPTION: str = "Sensor de humedad, lengua de suegra tipo hahnii"


def humidity_sensor() -> tuple[int, int]:
    """Enables the sensor, read data and conver into humidity percentage, finally, turn off the sensor

    Returns:
        tuple[int, int]: Lecture, Humidity percentage
    """

    adc = ADC(0)
    D0.on()

    lectures_range: int = MAX - MIN
    lecture: int = adc.read_u16()
    percentage: int = round(((MAX - lecture) / lectures_range) * 100)
    D0.off()

    return (lecture, 100 if percentage > 100 else percentage)


def create_sensor_in_api(sensor_info: dict[str, int | str]) -> bool:
    """POST on API to register the sensor

    Args:
        sensor_info (dict[str, int  |  str]): Sensor information

    Returns:
        bool: Registered sensor
    """
    api_response = requests.post(SENSOR_CREATE_URL, json=sensor_info)
    if api_response.status_code == 200:
        return True
    return False


def register_lecture_in_api(sensor_data: dict[str, int | str | tuple]) -> bool:
    api_response = requests.post(SENSOR_LECTURE_URL, json=sensor_data)
    print(api_response)
    if api_response == 200:
        return True
    return False


if __name__ == "__main__":
    D0.off()
    # Registar el sensor en la api
    sensor_info: dict[str, int | str] = {
        "id": SENSOR_ID,
        "name": SENSOR_NAME,
        "description": SENSOR_DESCRIPTION,
    }
    reg_sensor = create_sensor_in_api(sensor_info)

    print("Sensor creado" if reg_sensor else " Sensor ya existe en la db")
    time.sleep(10)

    print("Iniciando lectura")

    while True:
        humidity, h_percentage = humidity_sensor()
        date_time = time.localtime(time.time() + (-6 * 3600))
        year, month, day, hour, minute, second, *other_data = date_time
        date_time_stamp = (
            f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"
        )
        print(
            f"datetime: {date_time_stamp} Lectura: {humidity} - porcetaje: {h_percentage}"
        )
        # Aqui irá el POST a la API
        sensor_data: dict[str, int | str | tuple] = {
            "sensor_id": SENSOR_ID,
            "lecture": h_percentage,
            "date_time": (year, month, day, hour, minute, second),
        }
        reg_lecture = register_lecture_in_api(sensor_data)
        print(
            "Lectura registrada"
            if reg_lecture
            else "Algo falló al registrar la lectura"
        )

        time.sleep(5)
