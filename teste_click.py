import subprocess
import os
import time


env = os.environ.copy()

env["YDOTOOL_SOCKET"] = "/tmp/.ydotool_socket"


print("Iniciando teste...")


for i in range(5):

    subprocess.run(
        [
            "ydotool",
            "click",
            "1"
        ],
        env=env
    )

    print(f"Clique {i+1}")

    time.sleep(1)


print("Finalizado!")
