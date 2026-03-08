# This file is executed on every boot (including wake-boot from deepsleep)

import os
import time

import network  # type: ignore
from dotenv import load_dotenv  # type: ignore

load_dotenv()
SSID = os.getenv("SSID")
PASSWORD = os.getenv("PASSWORD")


def wifi_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("\n\n")
        print(f"Conectando a la red {SSID}")
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)

        # Intentar conectar
        attempts = 0
        while not sta_if.isconnected() and attempts < 10:
            time.sleep(1)
            attempts += 1

    if sta_if.isconnected():
        print("\nConexión exitosa!")
        print(f"Configuración de la red:\n{sta_if.ifconfig()}")
    else:
        print("\nNo se pudo conectar. Revisale papito.")


if __name__ == "__main__":
    wifi_connect()
