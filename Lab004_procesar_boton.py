"""
Author: Pedro Sanchez (mrchunckuee_electronics)
Blog:   http://mrchunckuee.blogspot.com/
"""
import gpiod
from gpiod.line import Direction, Value
import time

# Configuracion del hardware
CHIP_LEDS = '/dev/gpiochip1'
PINES_LEDS = [24, 22, 25, 23]   # LEDs ordenados -> GPIO1_D0, GPIO1_C6, GPIO1_D1, GPIO1_C7

CHIP_BOTON = '/dev/gpiochip2'
PIN_BOTON = 7                   # Boton en GPIO2_A7 (Pulsado = Value.ACTIVE)

VELOCIDAD = 0.2                 # Tiempo de animacion (200 ms)

print("Control de efectos LED con boton... Presiona Ctrl+C para detener.")

config_leds = {
    pin: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE)
    for pin in PINES_LEDS
}

config_boton = {
    PIN_BOTON: gpiod.LineSettings(direction=Direction.INPUT)
}

def GPIO_ClearLEDs(lineas_leds):
    for pin in PINES_LEDS:
        lineas_leds.set_value(pin, Value.INACTIVE)

def GPIO_GetButtonStatus(linea_boton, tiempo_espera, ultimo_estado_btn):

    paso = 0.02  # Muestra cada 20 ms
    tiempo_transcurrido = 0.0
    boton_presionado = False

    while tiempo_transcurrido < tiempo_espera:
        estado_actual = linea_boton.get_value(PIN_BOTON)
        
        # Deteccion paso de INACTIVE a ACTIVE
        if estado_actual == Value.ACTIVE and ultimo_estado_btn[0] == Value.INACTIVE:
            time.sleep(0.05) # Debouncing
            boton_presionado = True
            ultimo_estado_btn[0] = Value.ACTIVE
            break
            
        ultimo_estado_btn[0] = estado_actual
        time.sleep(paso)
        tiempo_transcurrido += paso

    return boton_presionado

# Configuramos GPIOs
with gpiod.request_lines(CHIP_LEDS, config=config_leds) as lineas_leds, \
     gpiod.request_lines(CHIP_BOTON, config=config_boton) as lineas_boton:

    modo = 0  # 0: Apagado, 1: Auto Fantastico, 2: Der, 3: Izq, 4: Intercalado
    ultimo_estado_btn = [Value.INACTIVE] # Estado previo del boton

    try:
        while True:
            # ----------------------------------------------------
            # MODO 0: TODO APAGADO
            # ----------------------------------------------------
            if modo == 0:
                GPIO_ClearLEDs(lineas_leds)
                while modo == 0:
                    if GPIO_GetButtonStatus(lineas_boton, 0.1, ultimo_estado_btn):
                        modo = 1
                        print("[INFO] Modo 1: Auto Fantastico")

            # ----------------------------------------------------
            # MODO 1: AUTO FANTASTICO
            # ----------------------------------------------------
            elif modo == 1:
                # Izquierda a Derecha
                for i in range(len(PINES_LEDS)):
                    GPIO_ClearLEDs(lineas_leds)
                    lineas_leds.set_value(PINES_LEDS[i], Value.ACTIVE)
                    if GPIO_GetButtonStatus(lineas_boton, VELOCIDAD, ultimo_estado_btn):
                        modo = 2
                        print("[INFO] Modo 2: Desplazamiento a la Derecha")
                        break
                
                if modo != 1: continue

                # Derecha a Izquierda
                for i in range(len(PINES_LEDS) - 2, 0, -1):
                    GPIO_ClearLEDs(lineas_leds)
                    lineas_leds.set_value(PINES_LEDS[i], Value.ACTIVE)
                    if GPIO_GetButtonStatus(lineas_boton, VELOCIDAD, ultimo_estado_btn):
                        modo = 2
                        print("[INFO] Modo 2: Desplazamiento a la Derecha")
                        break

            # ----------------------------------------------------
            # MODO 2: DESPLAZAMIENTO UN SENTIDO (Derecha)
            # ----------------------------------------------------
            elif modo == 2:
                for i in range(len(PINES_LEDS)):
                    GPIO_ClearLEDs(lineas_leds)
                    lineas_leds.set_value(PINES_LEDS[i], Value.ACTIVE)
                    if GPIO_GetButtonStatus(lineas_boton, VELOCIDAD, ultimo_estado_btn):
                        modo = 3
                        print("[INFO] Modo 3: Desplazamiento a la Izquierda")
                        break

            # ----------------------------------------------------
            # MODO 3: DESPLAZAMIENTO SENTIDO CONTRARIO (Izquierda)
            # ----------------------------------------------------
            elif modo == 3:
                for i in range(len(PINES_LEDS) - 1, -1, -1):
                    GPIO_ClearLEDs(lineas_leds)
                    lineas_leds.set_value(PINES_LEDS[i], Value.ACTIVE)
                    if GPIO_GetButtonStatus(lineas_boton, VELOCIDAD, ultimo_estado_btn):
                        modo = 4
                        print("[INFO] Modo 4: Intercalado")
                        break

            # ----------------------------------------------------
            # MODO 4: INTERCALADO ON / OFF
            # ----------------------------------------------------
            elif modo == 4:
                # Estado A: ON, OFF, ON, OFF
                for idx, pin in enumerate(PINES_LEDS):
                    lineas_leds.set_value(pin, Value.ACTIVE if idx % 2 == 0 else Value.INACTIVE)

                if GPIO_GetButtonStatus(lineas_boton, VELOCIDAD, ultimo_estado_btn):
                    modo = 0
                    print("[INFO] Modo 0: LEDs Apagados")
                    continue

                # Estado B: OFF, ON, OFF, ON
                for idx, pin in enumerate(PINES_LEDS):
                    lineas_leds.set_value(pin, Value.INACTIVE if idx % 2 == 0 else Value.ACTIVE)

                if GPIO_GetButtonStatus(lineas_boton, VELOCIDAD, ultimo_estado_btn):
                    modo = 0
                    print("[INFO] Modo 0: LEDs Apagados")

    except KeyboardInterrupt:
        print("\n[INFO] Script detenido.")
    finally:
        GPIO_ClearLEDs(lineas_leds)
        print("[INFO] LEDs apagados y lineas liberadas correctamente.")