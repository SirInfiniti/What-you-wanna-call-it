import board
import busio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.extensions.display import Display, SSD1306, TextEntry

keyboard = KMKKeyboard()

# 1. Add Modules
keyboard.modules.append(Layers())

# 2. Define Pins (Direct Wiring)
keyboard.direct_pins = [
    board.GP1,  # SW1
    board.GP0,  # SW2
    board.GP2,  # SW3
    board.GP26, # SW4
    board.GP27, # SW5
    board.GP28, # SW6
    board.GP4,  # SW7
    board.GP6,  # SW8
    board.GP7,  # SW9
]

# 3. Explicit I2C Setup for XIAO RP2040
# Based on your schematic: SCL = GP3, SDA = GP29
i2c_bus = busio.I2C(scl=board.GP3, sda=board.GP29)

display_driver = SSD1306(
    i2c=i2c_bus,
    device_address=0x3C,
)

# 4. OLED Display Configuration
# This tells the screen to show the current Layer name
display_extension = Display(
    display_driver=display_driver,
    width=128,
    height=32,
    entries=[
        TextEntry(text='Layer: ', x=0, y=0),
        TextEntry(text='Base', x=40, y=0, layer=0),
        TextEntry(text='Media', x=40, y=0, layer=1),
    ],
)
keyboard.extensions.append(display_extension)

# 5. Keymap with Layers
# SW9 (GP7) is used here as a "Momentary" switch to access Layer 1
keyboard.keymap = [
    # LAYER 0: Standard Numbers
    [
        KC.N1, KC.N2, KC.N3,
        KC.N4, KC.N5, KC.N6,
        KC.N7, KC.N8, KC.MO(1), # Hold SW9 to access Layer 1
    ],
    # LAYER 1: Media & Shortcuts
    [
        KC.VOLU, KC.MUTE, KC.VOLD,
        KC.MPRV, KC.MPLY, KC.MNXT,
        KC.COPY, KC.PSTE, KC.TRNS, # TRNS means "transparent" (inherits from Layer 0)
    ],
]

if __name__ == '__main__':
    keyboard.go()