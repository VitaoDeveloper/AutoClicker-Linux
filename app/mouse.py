import os
import subprocess
import time
import shutil

VALID_BUTTONS = {1, 2, 3}

_VENDOR_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "vendor", "ydotool"
)

_VENDORED_YDOTOOL = os.path.join(_VENDOR_DIR, "ydotool")
_VENDORED_YDOTOOLD = os.path.join(_VENDOR_DIR, "ydotoold")

_YDOTOOL_SOCKET_PATH = "/tmp/.ydotool_socket"

# app usa 1=esquerdo, 2=meio, 3=direito
_YDOTOOL_BUTTON_MAP = {1: "0xC0", 2: "0xC2", 3: "0xC1"}

_x11_controller = None
_daemon_process = None


class MouseError(Exception):
    """Erro ao tentar executar um clique de mouse."""


def _ydotool_binary():
    if os.path.isfile(_VENDORED_YDOTOOL) and os.access(_VENDORED_YDOTOOL, os.X_OK):
        return _VENDORED_YDOTOOL
    return shutil.which("ydotool") or "ydotool"


def _socket_is_alive(path):
    import socket as socket_module

    if not os.path.exists(path):
        return False

    sock = socket_module.socket(socket_module.AF_UNIX, socket_module.SOCK_STREAM)
    sock.settimeout(0.3)
    try:
        sock.connect(path)
        return True
    except OSError:
        return False
    finally:
        sock.close()


def _ensure_daemon_running():
    global _daemon_process

    if _socket_is_alive(_YDOTOOL_SOCKET_PATH):
        return

    # arquivo de socket órfão de uma execução anterior: remove antes de subir de novo
    if os.path.exists(_YDOTOOL_SOCKET_PATH):
        try:
            os.remove(_YDOTOOL_SOCKET_PATH)
        except OSError:
            pass

    if not (os.path.isfile(_VENDORED_YDOTOOLD) and os.access(_VENDORED_YDOTOOLD, os.X_OK)):
        return  # sem daemon vendorizado, deixa o erro normal acontecer e avisar o usuário

    _daemon_process = subprocess.Popen(
        [_VENDORED_YDOTOOLD, f"--socket-path={_YDOTOOL_SOCKET_PATH}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    for _ in range(50):  # espera até 5s o socket aparecer
        if os.path.exists(_YDOTOOL_SOCKET_PATH):
            break
        time.sleep(0.1)


def get_session():
    return os.environ.get("XDG_SESSION_TYPE", "")


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

        _ensure_daemon_running()

        env = os.environ.copy()
        env["YDOTOOL_SOCKET"] = _YDOTOOL_SOCKET_PATH

        try:
            subprocess.run(
                [_ydotool_binary(), "click", _YDOTOOL_BUTTON_MAP[button]],
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

            mouse.click(buttons[button])
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

    _ensure_daemon_running()

    env = os.environ.copy()
    env["YDOTOOL_SOCKET"] = _YDOTOOL_SOCKET_PATH

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