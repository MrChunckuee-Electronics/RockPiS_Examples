"""
Author: Pedro Sanchez (mrchunckuee_electronics)
Blog:   http://mrchunckuee.blogspot.com/
"""
import gpiod
from gpiod.line import Direction, Value
import time

# Configuracion del hardware
RUTA_CHIP = '/dev/gpiochip1'
PINES = [24, 22, 25, 23]    # Orden de LEDs ordenados
VELOCIDAD = 0.2             # Tiempo entre cada paso (200 ms)

print("LEDs con efecto del Auto Fantastico... Presiona Ctrl+C para detener.")

config_pines = {
    pin: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE)
    for pin in PINES
}

# Configuramos GPIOs
with gpiod.request_lines(RUTA_CHIP, config=config_pines) as lineas:
    try:
        while True:
            # Movimiento de Izquierda a Derecha
            for i in range(len(PINES)):
                lineas.set_value(PINES[i], Value.ACTIVE)
                time.sleep(VELOCIDAD)
                lineas.set_value(PINES[i], Value.INACTIVE)

            # Movimiento de Derecha a Izquierda
            for i in range(len(PINES) - 2, 0, -1):
                lineas.set_value(PINES[i], Value.ACTIVE)
                time.sleep(VELOCIDAD)
                lineas.set_value(PINES[i], Value.INACTIVE)

    except KeyboardInterrupt:
        print("\n[INFO] Script detenido. Apagando todos los LEDs...")
        for pin in PINES:
            lineas.set_value(pin, Value.INACTIVE)

print("[INFO] Script terminado, pines liberados.")
