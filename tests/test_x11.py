from pynput.mouse import Controller, Button
import time


mouse = Controller()

print("Movendo mouse em 3 segundos...")

time.sleep(3)

mouse.click(Button.left)

print("Clique realizado!")
