from clicker import AutoClicker


def status(valor):

    print("Evento:", valor)


print("Iniciando AutoClicker")


bot = AutoClicker(
    interval=1,
    amount=5,
    callback=status
)


bot.start()


bot.thread.join()


print("Finalizado")