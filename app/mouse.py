import os
import subprocess


VALID_BUTTONS = {1, 2, 3}


_x11_controller = None

class MouseError(Exception):
    """Erro ao tentar executar um clique de mouse."""


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


def click_burst(button=1, count=1, interval=0.1):
    """Executa múltiplos cliques em uma única invocação do ydotool,
    evitando spawnar um processo novo por clique (Wayland)."""

    if button not in VALID_BUTTONS:
        raise MouseError(
            f"Botão inválido: {button}. Use 1 (esquerdo), 2 (meio) ou 3 (direito)."
        )

    base = {1: 0x00, 2: 0x02, 3: 0x01}[button]  # left, middle, right
    click_code = 0xC0 | base  # 0xC0 = bits de "down" + "up"

    next_delay_ms = max(1, int(interval * 1000))

    env = os.environ.copy()
    env["YDOTOOL_SOCKET"] = "/tmp/.ydotool_socket"

    try:
        return subprocess.Popen(
            [
                "ydotool", "click",
                "--repeat", str(count),
                "--next-delay", str(next_delay_ms),
                f"0x{click_code:02x}",
            ],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        raise MouseError(
            "ydotool não encontrado. Instale o pacote 'ydotool' para usar o clicker no Wayland."
        )