from PyQt6.QtWidgets import QApplication

from Logic import *
from AutoClicker import *

def main():
    application = QApplication([])
    window = Logic()
    window.show()
    application.exec()


if __name__ == "__main__":
    main()