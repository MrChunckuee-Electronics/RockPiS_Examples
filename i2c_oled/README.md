# RockPiS: I2C OLED 128x64 scripts
Example scripts for controlling a 128x64 OLED on our Rock Pi S.

## Hardware Connection

- [GPIO Header](https://docs.radxa.com/en/rockpi/rockpis/hardware/pin-gpio)

## Setup

Step 1 - Enable I2C Overlay

rsetup # Overlays => Yes => Manage overlays => Select "Enable I2C8-M2" => Ok => Ok => Cancel => Cancel
reboot

Step 2 - Install Python's dependencies

sudo apt install python-periphery pillow

## Documentation & Tutorial
For a detailed implementation explanation and step-by-step guide, you can review the following examples:
* [https://mrchunckuee.blogspot.com/p/rock-pi-s-mini-computer-with-rockchip.html](https://mrchunckuee.blogspot.com/p/rock-pi-s-mini-computer-with-rockchip.html)
