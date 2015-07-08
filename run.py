import argparse
from app import app

parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true', default=False, dest='debug')
args = parser.parse_args()

if __name__ == '__main__':
    app.run(threaded=True, debug=args.debug)
