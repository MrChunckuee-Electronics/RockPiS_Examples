"""
Author: Pedro Sanchez (mrchunckuee_electronics)
Blog:   http://mrchunckuee.blogspot.com/
"""

from textwrap import wrap

from periphery import I2C
from PIL import Image, ImageDraw, ImageFont

class OledI2C:
    """OledI2C Class"""
    def __init__(self, bus:str="/dev/i2c-1", address:int=0x3C) -> None:
        """Initialize"""
        self.bus = bus
        self.address = address
        self.i2c = I2C(self.bus)
        self.width = 128
        self.height = 64
        self.font = ImageFont.load_default() #default text on PIL
        self.OLED_Initialize()

    def SSD1306_Command(self, cmd:int) -> None:
        """SSD1306 Command"""
        msg = I2C.Message([0x00, cmd])
        self.i2c.transfer(self.address, [msg])

    def OLED_Initialize(self) -> None:
        """Initialize OLED"""
        commands = [
            0xAE,       # Display off
            0x00,       # Set lower column address
            0x10,       # Set higher column address
            0x40,       # Set display start line
            0xD5, 0x80, # Set display clock divide ratio/oscillator frequency
            0xA8, 0x3F, # Set multiplex ratio for 64 rows (0x3F = 63)
            0xD3, 0x00, # Set display offset
            0x8D, 0x14, # Enable charge pump regulator
            0x20, 0x00, # Memory mode
            0xA1,       # Set segment remap
            0xC8,       # Set COM output scan direction
            0xDA, 0x12, # COM pins config (sequential for 64px)
            0x81, 0xCF, # Set contrast control
            0xD9, 0xF1, # Set pre-charge period
            0xDB, 0x40, # Set VCOMH deselect level
            0xA4,       # Display resume
            0xB0,       # Set page address
            0xA6,       # Normal display
            0xAF        # Display on
        ]
        for cmd in commands:
            self.SSD1306_Command(cmd)
        self.clear_display()

    def clear_display(self) -> None:
        """Clear display"""
        # Clear all 8 pages (64px height)
        for page in range(8):
            self.SSD1306_Command(0xB0 + page)
            self.SSD1306_Command(0x00)
            self.SSD1306_Command(0x10)
            # Send zeros per page in one transfer
            data = [0x40] + [0x00] * self.width
            msg = I2C.Message(data)
            self.i2c.transfer(self.address, [msg])

    def display_text(self, text: str) -> None:
        """Display text"""
        image = Image.new("1", (self.width, self.height))
        draw = ImageDraw.Draw(image)

        # Adjust text wrapping and positioning
        lines = wrap(text, width=21) # ~21 chars per line for 8px font
        y_text = 0
        font_size = 8  # Adjust according to the height of your source.
        for line in lines:
            if y_text + font_size > self.height:
                break
            draw.text((0, y_text), line, font=self.font, fill=255)
            y_text += font_size

        # Send entire pages in single transfers
        for page in range(8):
            self.SSD1306_Command(0xB0 + page)
            self.SSD1306_Command(0x00)
            self.SSD1306_Command(0x10)

            page_data = []
            for col in range(self.width):
                byte = 0
                for bit in range(8):
                    try:
                        pixel = image.getpixel((col, page * 8 + bit))
                    except IndexError:
                        pixel = 0
                    byte |= (pixel & 0x1) << bit
                page_data.append(byte)

            msg = I2C.Message([0x40] + page_data)
            self.i2c.transfer(self.address, [msg])

    def close(self) -> None:
        """Close"""
        self.i2c.close()

# Execute
oled = OledI2C()
oled.display_text("Testing the OLED to display a long text; creating the OledI2C class. MrChunckuee Electronics!!")
oled.close()
