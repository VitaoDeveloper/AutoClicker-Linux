from app.mouse import click

import time


print("Teste iniciado")


for i in range(5):

    click()

    print(
        "Clique",
        i+1
    )

    time.sleep(1)


print("Fim")
