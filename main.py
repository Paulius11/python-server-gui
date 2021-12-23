from time import sleep

from PyQt5 import QtWidgets, uic
import sys
import os.path
from PyQt5.QtWidgets import QFileDialog
import server
import socket
import logging
logging.basicConfig(format="%(message)s", level=logging.INFO)


from threading import *
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(os.path.join(PROJECT_PATH, 'server.ui'), self)
        self.selected_folder = "./"

        self.browse = self.findChild(QtWidgets.QPushButton, 'pushButton')  # Find the button
        self.browse.clicked.connect(self.select_file_button_pressed)

        self.start = self.findChild(QtWidgets.QPushButton, 'pushButton_2')  # Find the button
        self.start.clicked.connect(self.thread)

        self.label_share_dir = self.findChild(QtWidgets.QLabel, 'label_2')  # Find the button
        self.label_ip = self.findChild(QtWidgets.QLabel, 'label_5')  # Find the button

        self.label_status = self.findChild(QtWidgets.QLabel, 'label_status')


        self.show()

    def thread(self):
        t1=Thread(target=self.start_server)
        t1.start()
        self.label_ip.setText(f'http://{self.get_ip()}:{8000}')
        self.label_status.setText(f"Server started.")
        self.label_status.setStyleSheet("background-color: lightgreen")


    def get_ip(self, remote_server="google.com"):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect((remote_server, 80))
            return s.getsockname()[0]


    def get_folder(self):
        f_name = QFileDialog.getExistingDirectory(self, "Open this bad boy", application_path)
        return f_name

    def select_file_button_pressed(self):
        self.selected_folder = self.get_folder()
        print(self.selected_folder)
        self.label_share_dir.setText(self.selected_folder)

    def start_server(self):

        logging.info("Starting server...")
        http_server = server.HttpServer(path=self.selected_folder, port=8000)
        http_server.start_server()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
