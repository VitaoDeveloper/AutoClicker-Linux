import os
import subprocess
import time
import shutil

VALID_BUTTONS = {1, 2, 3}

_VENDORED_YDOTOOL = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "vendor", "ydotool", "ydotool"
)

_YDOTOOL_BUTTON_MAP = {1: "1", 2: "3", 3: "2"}  # app usa 1=esq,2=meio,3=dir; esse ydotool usa 1=esq,2=dir,3=meio

_x11_controller = None

class MouseError(Exception):
    """Erro ao tentar executar um clique de mouse."""


def _ydotool_binary():
    if os.path.isfile(_VENDORED_YDOTOOL) and os.access(_VENDORED_YDOTOOL, os.X_OK):
        return _VENDORED_YDOTOOL
    return shutil.which("ydotool") or "ydotool"

def get_session():

    return os.environ.get(
        "XDG_SESSION_TYPE",
        ""
    )


def _get_x11_controller():
    global _x11_controller
    if _x11_controller is None:
        from pynput.mouse import Controller
        _x11_controller = Controller()
    return _x11_controller

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
                    _YDOTOOL_BUTTON_MAP[button]  
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

            mouse = _get_x11_controller()

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


def click_burst(button=1, count=1, interval=0.1, running_flag=None, on_click=None):
    """Clica repetidamente via ydotool, um processo por clique.
    Sem --repeat porque nem toda build do ydotool suporta essa flag."""

    if button not in VALID_BUTTONS:
        raise MouseError(
            f"Botão inválido: {button}. Use 1 (esquerdo), 2 (meio) ou 3 (direito)."
        )

    env = os.environ.copy()
    env["YDOTOOL_SOCKET"] = "/tmp/.ydotool_socket"

    clicked = 0
    try:
        while running_flag is None or running_flag():
            subprocess.run(
                [_ydotool_binary(), "click", _YDOTOOL_BUTTON_MAP[button]],
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            clicked += 1

            if on_click:
                on_click(clicked)

            if count and clicked >= count:
                break

            time.sleep(interval)
    except FileNotFoundError:
        raise MouseError(
            "ydotool não encontrado. Instale o pacote 'ydotool' para usar o clicker no Wayland."
        )
    except subprocess.CalledProcessError as error:
        raise MouseError(
            "Falha ao executar ydotool. Verifique se o daemon 'ydotoold' está rodando. "
            f"Detalhes: {error.stderr.strip() if error.stderr else error}"
        )
    return clicked