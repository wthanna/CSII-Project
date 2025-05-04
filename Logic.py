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

        self.begin = time.time()
        self.running = False
        self.delay_lineEdit.setText("1")
        self.startClick_lineEdit.setText("a")
        self.endClick_lineEdit.setText("b")
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
            delay_text = self.delay_lineEdit.text().strip()
            self.delay = float(delay_text) if delay_text else 1.0
            start_key = self.startClick_lineEdit.text().lower()
            stop_key = self.endClick_lineEdit.text().lower()

            if len(start_key) != 1 or len(stop_key) != 1 or not start_key.strip() or not stop_key.strip():
                self.error_message_lable.setText("Start/Stop keys must be 1 non-space character only.")
                return

            if self.delay <= 0:
                self.error_message_lable.setText("Delay must be grater than 0.")
                return

            if start_key == stop_key:
                self.error_message_lable.setText("Start and Stop keys must be different.")
            self.start_hotkey = start_key
            self.stop_hotkey = stop_key

        except ValueError:
            self.error_message_lable.setText("Invalid delay. Must be a number.")
            return

        self.begin = time.time()
        self.running = True
        self.start_pushButton.setEnabled(False)
        self.end_pushButton.setEnabled(True)
        self.status_label.setText("running...")
        self.runTime_label.setText(f"running...")
        self.error_message_lable.setText("")
        threading.Thread(target=self.click_loop, daemon=True).start()

    def stop_clicking(self):
        self.running = False
        self.start_pushButton.setEnabled(True)
        self.end_pushButton.setEnabled(False)
        self.status_label.setText("stopped")
        time.sleep(1)
        end = time.time()
        self.runTime_label.setText(f"{(end - self.begin):.2f}")

        try:
            with open("clicker_runtime_log.txt", "a") as log_file:
                log_file.write(f"Session duration: {(end - self.begin):.2f} seconds\n")
        except Exception as e:
            self.error_message_lable.setText(f"Log Error: {e}")


