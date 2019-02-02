from random import choice
import os

# get file path to find dependent files
dirname = os.path.dirname(__file__)


def get_bro():
    brofile = os.path.join(dirname, 'files/bro.txt')
    with open(brofile) as f:
        names = f.read()
    return choice(names.split('\n'))


if __name__ == '__main__':
    print("MongBroDB")
    while True:
        # cont = (input("'exit'/'quit' to exit ") or 'true')
        if ((input("'exit'/'quit' to exit ") or 'true').lower() in ['exit', 'quit']):
            break
        print(get_bro())
    print("Goodbye")
