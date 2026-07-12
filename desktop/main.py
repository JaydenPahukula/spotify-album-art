import argparse
from src.app import App

parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true", help="run in debug mode")

if __name__ == "__main__":
    args = parser.parse_args()

    app = App(args)
    app.run()
