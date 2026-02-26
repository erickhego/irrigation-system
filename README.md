# COMMANDS

- `ls /dev/tty.*`: Lista los dispositivos conectados por usb.
- `screen /dev/tty.usbserial-21130 115200`: Monitor serial y ejecución rápida de python dentro del microcontrolador.
- `ampy --port /dev/tty.usbserial-21130 put boot.py`: sube el archivo al microcontrolador.
- `ampy --port /dev/tty.usbserial-21130 get boot.py boot.py`: Descarga un programa y los guarda en el archivo especificado.
