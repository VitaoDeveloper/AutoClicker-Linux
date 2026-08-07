import sys

from app.gui import AutoClickerApp


def main():
    app = AutoClickerApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
