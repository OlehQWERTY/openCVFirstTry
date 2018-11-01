from gpiozero import LED
from time import sleep

out = LED(17)

while True:
    out.on()
    sleep(1)
    out.off()
    sleep(1)