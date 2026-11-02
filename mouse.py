import spidev
import uinput 
import time
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000
mouse = uinput.Device([
    uinput.REL_X,
    uinput.REL_Y,
    uinput.BTN_LEFT,
])
def read_adc(ch):
    r = spi.xfer2([1, (8 + ch) <<4, 0])
    return ((r[1] & 3) << 8) + r[2]

CENTER = 512
DEADZONE = 40

while True:
    x = read_adc(0)
    y = read_adc(1)
    
    dx = x - CENTER
    dy = y - CENTER
    
    if abs(dx) < DEADZONE:
        dx = 0
    if abs(dy) < DEADZONE:
        dy = 0
    dx = int((dx / 512) * 12)
    dy = int((dy / 512) * 12)

    if dx or dy:
        mouse.emit(uinput.REL_X, dx, syn=False)
        mouse.emit(uinput.REL_Y, -dy)
    time.sleep(0.01)
    
