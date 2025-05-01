from PyQt6.QtWidgets import QMainWindow
from pynput.keyboard import Listener, KeyCode
from gui import Ui_autoclicker
import time
import threading
from pynput.mouse import Button, Controller
import keyboard

mouse = Controller()

class Logic(QMainWindow, Ui_autoclicker):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.running = False
        self.delay = .001
        self.start_hotkey = "a"
        self.stop_hotkey = "b"

        self.start_pushButton.clicked.connect(self.start_clicking)
        self.end_pushButton.clicked.connect(self.stop_clicking)
        self.end_pushButton.setEnabled(False)

        threading.Thread(target=self.hotkey_listener, daemon=True).start()

        self.error_message_lable.setText("")
        self.status_label.setText("Off")

    def hotkey_listener(self):
        while True:
            if keyboard.is_pressed(self.start_hotkey):
                if not self.running:
                    self.start_clicking()
                    time.sleep(0.5)  # Debounce
            if keyboard.is_pressed(self.stop_hotkey):
                if self.running:
                    self.stop_clicking()
                    time.sleep(0.5)

    def click_loop(self):
        while self.running:
            mouse.click(Button.left)
            time.sleep(self.delay)

    def start_clicking(self):
        try:
            self.delay = float(self.delay_lineEdit.text())
            self.start_hotkey = self.startClick_lineEdit.text().lower()
            self.stop_hotkey = self.endClick_lineEdit.text().lower()
        except ValueError:
            self.error_message_lable.setText("Error")
            return

        self.running = True
        self.start_pushButton.setEnabled(False)
        self.end_pushButton.setEnabled(True)
        self.status_label.setText("running...")
        threading.Thread(target=self.click_loop, daemon=True).start()

    def stop_clicking(self):
        self.running = False
        self.start_pushButton.setEnabled(True)
        self.end_pushButton.setEnabled(False)
        self.status_label.setText("stopped")

    #def clear_input(self):
    #    self.lineEdit_food.clear()
    #    self.lineEdit_drink.clear()
    #    self.lineEdit_desert.clear()
    #    self.radioButton.setChecked(True)
    #    self.label_summary.setText("")
    #    self.label_summarybox.setText("")
