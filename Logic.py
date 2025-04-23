from PyQt6.QtWidgets import QMainWindow
from pynput.keyboard import Listener, KeyCode
from gui import Ui_autoclicker
import time
import threading
from pynput.mouse import Button, Controller


class Logic(QMainWindow, Ui_autoclicker):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #self.Savebutton.connect(lambda : self.submit)
        self.confirm_pushButton.clicked.connect(self.confirm)#
        self.default_pushButton.clicked.connect(self.clear_input)#

        self.error_message_lable.setText("")
        self.status_label.setText("Off")


    def confirm(self):
        try:
            start_key = self.startClick_lineEdit.text().strip()
            start_key = self.startClick_lineEdit.KeyCode(char="").strip()
            stop_key = self.endClick_lineEdit.text().strip()
            delay = self.delay_lineEdit.text().strip()
            delay = float(delay)


            tip_per = .10
            if self.radioButton_2.isChecked():
                tip_per = .15
            elif self.radioButton_3.isChecked():
                tip_per = .2


            meal_total = food + drink + dessert
            tax = meal_total * .10
            tip = (meal_total + tax) * tip_per
            total = meal_total + tax + tip

            summary = (f"Food:                         ${food:.2f}\n"
                       f"Drink:                         ${drink:.2f}\n"
                       f"Dessert:                     ${dessert:.2f}\n"
                       f"Tax:                            ${tax:.2f}\n"
                       f"Tip:                            ${tip:.2f}\n\n"
                       f"TOTAL:                       ${total:.2f}")
            self.label_summary.setText("SUMMARY")
            self.label_summarybox.setText(summary)

        except ValueError:
            self.label_summarybox.setText(f"Food, drink, and dessert\nmust be numeric.")

    def clear_input(self):
        self.lineEdit_food.clear()
        self.lineEdit_drink.clear()
        self.lineEdit_desert.clear()
        self.radioButton.setChecked(True)
        self.label_summary.setText("")
        self.label_summarybox.setText("")
