# RockPiS: I2C OLED 128x64 scripts
Example scripts for controlling a 128x64 OLED on our Rock Pi S.

| # | Name Script | Description | 
| :--- | :--- | :--- |
| 1 | Lab001_I2C_oled_short_text.py | Displays a short text |
| 2 |  |  |
| 3 |  |  |

## Hardware Connection

| Rock Pi S: # Pin | Rock Pi S: Function | OLED Pinout|
| :--- | :--- | :--- |
| 1 | +3V3 | VDD |
| 3 | I2C1_SDA | SDA |
| 5 | I2C1_SCL | SCL |
| 6 | GND | GND |


- [GPIO Header](https://docs.radxa.com/en/rockpi/rockpis/hardware/pin-gpio)

## Setup

### Step 1 - Enable I2C Overlay

``` python
rsetup => Overlays => Yes => Manage overlays => Select "Enable I2C1" => Ok => Ok => Cancel => Cancel
sudo reboot
```

### Step 2 - Install Python's dependencies

``` python
sudo apt install python-periphery pillow
```

## Documentation & Tutorial
For a detailed implementation explanation and step-by-step guide, you can review the following examples:
* [https://mrchunckuee.blogspot.com/p/rock-pi-s-mini-computer-with-rockchip.html](https://mrchunckuee.blogspot.com/p/rock-pi-s-mini-computer-with-rockchip.html)
