import threading
import time

from .mouse import click
from .state import ClickerState

class AutoClicker:

    def __init__(self, interval=0.1, button=1, amount=0, callback=None):

        self.interval = interval
        self.button = button
        self.amount = amount
        self.callback = callback

        self.clicks = 0

        self.running = False
        self.thread = None
        self.state = ClickerState.IDLE

    def start(self):

        if self.running:
            return

        self.running = True
        self.state = ClickerState.RUNNING

        self.thread = threading.Thread(target=self._run)

        self.thread.start()

    def stop(self):

        self.running = False
        self.state = ClickerState.STOPPED


    def _run(self):

        self.clicks = 0

        while self.running:

            click(self.button)

            self.clicks += 1

            if self.callback:
                self.callback(self.clicks)
            else:
                print(f"Clique {self.clicks}")


            if (
                self.amount > 0
                and self.clicks >= self.amount
            ):
                break


            time.sleep(
                self.interval
            )


        self.running = False

        if self.state != ClickerState.STOPPED:
            self.state = ClickerState.FINISHED


        if self.callback:
            self.callback("finished")