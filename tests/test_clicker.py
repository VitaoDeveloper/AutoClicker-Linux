from app.clicker import AutoClicker
from app.config import load_config

config = load_config()

def status(valor):

    print("Evento:", valor)


print("Iniciando AutoClicker")


bot = AutoClicker(
    interval=config["interval"],
    button=config["button"],
    amount=config["amount"],
    callback=status
)


print("Estado inicial:", bot.state)


bot.start()

bot.thread.join()


print("Estado final:", bot.state)


print("Finalizado")