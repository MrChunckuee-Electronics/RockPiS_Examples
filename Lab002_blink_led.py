"""
Author: Pedro Sanchez (mrchunckuee_electronics)
Blog:   http://mrchunckuee.blogspot.com/
"""
import gpiod
from gpiod.line import Direction, Value
import time

# Configuracion del hardware
PIN_LINEA = 22
RUTA_CHIP = '/dev/gpiochip1'

print("Parpadeando el LED en el PIN_22... Presiona Ctrl+C para detener.")

try:
    # Usamos submodulo gpiod.line
    with gpiod.request_lines(
        RUTA_CHIP,
        config={
            PIN_LINEA: gpiod.LineSettings(
                direction=Direction.OUTPUT,
                output_value=Value.INACTIVE)
            }
        ) as lineas:
        while True:
            lineas.set_value(PIN_LINEA, Value.ACTIVE)    # LED - ON
            time.sleep(0.5)
            lineas.set_value(PIN_LINEA, Value.INACTIVE)  # LED - OFF
            time.sleep(0.5)
except KeyboardInterrupt:
    print("\n[INFO] Script detenido. PIN_22 liberado y LED apagado correctamente.")
