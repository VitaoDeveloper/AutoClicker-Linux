import time

from clicker import AutoClicker


def status(valor):
    print("Evento:", valor)


bot = AutoClicker(
    interval=0.5,
    callback=status
)


print("Estado inicial:", bot.state)

bot.start()

time.sleep(3)

print("Parando...")

bot.stop()

bot.thread.join()

print("Estado depois do stop:", bot.state)