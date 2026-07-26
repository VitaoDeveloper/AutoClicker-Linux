import os
import subprocess


def get_session():

    return os.environ.get(
        "XDG_SESSION_TYPE",
        ""
    )


def click(button=1):

    session = get_session()


    # Wayland
    if session == "wayland":

        env = os.environ.copy()

        env["YDOTOOL_SOCKET"] = (
            "/tmp/.ydotool_socket"
        )

        subprocess.run(
            [
                "ydotool",
                "click",
                str(button)
            ],
            env=env
        )


    # X11
    elif session == "x11":

        from pynput.mouse import Controller, Button

        mouse = Controller()


        buttons = {
            1: Button.left,
            2: Button.middle,
            3: Button.right
        }


        mouse.click(
            buttons[button]
        )


    else:

        raise Exception(
            f"Sessão não suportada: {session}"
        )
