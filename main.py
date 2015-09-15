from gui import Main
from game import Table


def main():
    game = Main(Table())
    game.run()

if __name__ == '__main__':
    main()
