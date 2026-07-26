import os
import subprocess


VALID_BUTTONS = {1, 2, 3}


class MouseError(Exception):
    """Erro ao tentar executar um clique de mouse."""


def get_session():

    return os.environ.get(
        "XDG_SESSION_TYPE",
        ""
    )


def click(button=1):

    if button not in VALID_BUTTONS:
        raise MouseError(
            f"Botão inválido: {button}. Use 1 (esquerdo), 2 (meio) ou 3 (direito)."
        )

    session = get_session()


    # Wayland
    if session == "wayland":

        env = os.environ.copy()

        env["YDOTOOL_SOCKET"] = (
            "/tmp/.ydotool_socket"
        )

        try:
            subprocess.run(
                [
                    "ydotool",
                    "click",
                    str(button)
                ],
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError:
            raise MouseError(
                "ydotool não encontrado. Instale o pacote 'ydotool' para usar o clicker no Wayland."
            )
        except subprocess.CalledProcessError as error:
            raise MouseError(
                "Falha ao executar ydotool. Verifique se o daemon 'ydotoold' está rodando. "
                f"Detalhes: {error.stderr.strip() if error.stderr else error}"
            )


    # X11
    elif session == "x11":

        try:
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
        except ImportError:
            raise MouseError(
                "pynput não está instalado. Rode 'pip install -r requirements.txt'."
            )
        except Exception as error:
            raise MouseError(
                f"Falha ao executar clique via pynput: {error}"
            )


    else:

        raise MouseError(
            f"Sessão não suportada: {session or 'desconhecida'}"
        )
