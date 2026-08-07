import threading
import select

from .mouse import get_session


class HotkeyError(Exception):
    """Erro ao registrar ou escutar um atalho global de teclado."""


# Nome amigável -> (nome do atalho no pynput, nome do keycode no evdev)
KEY_MAP = {
    "f1": ("f1", "KEY_F1"),
    "f2": ("f2", "KEY_F2"),
    "f3": ("f3", "KEY_F3"),
    "f4": ("f4", "KEY_F4"),
    "f5": ("f5", "KEY_F5"),
    "f6": ("f6", "KEY_F6"),
    "f7": ("f7", "KEY_F7"),
    "f8": ("f8", "KEY_F8"),
    "f9": ("f9", "KEY_F9"),
    "f10": ("f10", "KEY_F10"),
    "f11": ("f11", "KEY_F11"),
    "f12": ("f12", "KEY_F12"),
    "pause": ("pause", "KEY_PAUSE"),
    "scroll_lock": ("scroll_lock", "KEY_SCROLLLOCK"),
}

DEFAULT_HOTKEY = "f6"


class GlobalHotkey:
    """
    Escuta uma tecla globalmente (mesmo com a janela sem foco) e chama
    `on_trigger` sempre que ela for pressionada.

    X11  -> pynput.keyboard.GlobalHotKeys
    Wayland -> leitura direta dos dispositivos em /dev/input via evdev
               (pynput não recebe eventos globais no Wayland puro)
    """

    def __init__(self, key=DEFAULT_HOTKEY, on_trigger=None):
        key = key.lower()

        if key not in KEY_MAP:
            raise HotkeyError(
                f"Tecla de atalho não suportada: {key}. "
                f"Opções: {', '.join(KEY_MAP)}"
            )

        self.key = key
        self.on_trigger = on_trigger
        self._backend = None

    def start(self):
        session = get_session()

        if session == "x11":
            self._backend = _X11HotkeyBackend(self.key, self.on_trigger)
        elif session == "wayland":
            self._backend = _EvdevHotkeyBackend(self.key, self.on_trigger)
        else:
            raise HotkeyError(
                f"Sessão não suportada para atalhos globais: {session or 'desconhecida'}"
            )

        self._backend.start()

    def stop(self):
        if self._backend:
            self._backend.stop()
            self._backend = None


class _X11HotkeyBackend:

    def __init__(self, key, on_trigger):
        self.key = key
        self.on_trigger = on_trigger
        self._listener = None

    def start(self):
        try:
            from pynput import keyboard
        except ImportError:
            raise HotkeyError(
                "pynput não está instalado. Rode 'pip install -r requirements.txt'."
            )

        pynput_name, _ = KEY_MAP[self.key]
        combo = f"<{pynput_name}>"

        def _fire():
            if self.on_trigger:
                self.on_trigger()

        try:
            self._listener = keyboard.GlobalHotKeys({combo: _fire})
            self._listener.start()
        except Exception as error:
            raise HotkeyError(
                f"Falha ao registrar atalho global via pynput: {error}"
            )

    def stop(self):
        if self._listener:
            self._listener.stop()
            self._listener = None


class _EvdevHotkeyBackend:

    def __init__(self, key, on_trigger, device_finder=None):
        self.key = key
        self.on_trigger = on_trigger
        # Permite injetar uma função de busca de dispositivos nos testes
        self._device_finder = device_finder or self._find_keyboards

        self.running = False
        self.thread = None
        self.devices = []
        self._ecodes = None
        self._keycode = None

    def start(self):
        try:
            from evdev import ecodes
        except ImportError:
            raise HotkeyError(
                "evdev não está instalado. Rode 'pip install -r requirements.txt'."
            )

        self._ecodes = ecodes
        _, evdev_name = KEY_MAP[self.key]
        self._keycode = getattr(ecodes, evdev_name)

        self.devices = self._device_finder(self._keycode)

        if not self.devices:
            raise HotkeyError(
                "Nenhum teclado acessível encontrado em /dev/input. "
                "Adicione seu usuário ao grupo 'input' "
                "(sudo usermod -aG input $USER, depois faça logout/login) "
                "ou rode como root."
            )

        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _find_keyboards(self, keycode):
        from evdev import InputDevice, list_devices

        found = []
        for path in list_devices():
            try:
                dev = InputDevice(path)
            except (PermissionError, OSError):
                continue

            caps = dev.capabilities().get(self._ecodes.EV_KEY, [])
            if keycode in caps:
                found.append(dev)

        return found

    def _run(self):
        fd_to_device = {dev.fd: dev for dev in self.devices}

        while self.running:
            try:
                ready, _, _ = select.select(
                    list(fd_to_device.keys()), [], [], 0.5
                )
            except (OSError, ValueError):
                break

            for fd in ready:
                dev = fd_to_device.get(fd)
                if dev is None:
                    continue

                try:
                    for event in dev.read():
                        self._handle_event(event)
                except (OSError, BlockingIOError):
                    continue

    def _handle_event(self, event):
        # value == 1 é o key-down (0 é key-up, 2 é repeat)
        if (
            event.type == self._ecodes.EV_KEY
            and event.code == self._keycode
            and event.value == 1
        ):
            if self.on_trigger:
                self.on_trigger()

    def stop(self):
        self.running = False

        if self.thread:
            self.thread.join(timeout=1)
            self.thread = None

        for dev in self.devices:
            try:
                dev.close()
            except Exception:
                pass

        self.devices = []
