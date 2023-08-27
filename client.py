import os
import sys
import requests
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
from notifypy import Notify


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
class ResultReceiver(QtCore.QObject):
    resultReceived = QtCore.pyqtSignal(str)


class ServerWorker(QtCore.QRunnable):
    def __init__(self, serverip, isratelimit, receiver):
        super().__init__()
        self.serverip = serverip
        self.isratelimit = isratelimit
        self.receiver = receiver
        self.is_running = True
        self.sentnotif = False
        self.notification = Notify()

    def stop(self):
        self.is_running = False

    def run(self):
        while self.is_running:
            try:
                response = requests.get(self.serverip, timeout=3)
                data = response.text.strip()
                self.receiver.resultReceived.emit(data)
                if not self.sentnotif:
                    self.notification.title = "osu!papamobil"
                    self.notification.message = f"Connected to {str(self.serverip)}"
                    self.notification.audio = resource_path("notifysound.wav")
                    self.notification.send()
                    self.sentnotif = True
            except requests.exceptions.Timeout:
                pass
            except requests.exceptions.RequestException as e:
                print("Error during request:", e)

            QtCore.QThread.msleep(5000)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("gui.ui", self)
        self.connectbutton.clicked.connect(self.server_connect)
        self.thread_pool = QtCore.QThreadPool()
        self.connected = False
        self.dataold = None
        self.notification = Notify()

    def server_connect(self):
        serverip = self.textEdit.toPlainText()
        isratelimit = False
        if not self.connected:
            self.result_receiver = ResultReceiver()
            self.worker = ServerWorker(serverip, isratelimit, self.result_receiver)
            self.result_receiver.resultReceived.connect(self.handle_result)
            self.thread_pool.start(self.worker)

            self.connectbutton.setText("Disconnect")
            self.textEdit.setReadOnly(True)
            self.connected = True
        else:
            self.worker.stop()
            self.worker = None

            self.thread_pool.clear()

            self.result_receiver = None

            self.connectbutton.setText("Connect")
            self.textEdit.setReadOnly(False)
            self.connected = False

    def handle_result(self, result):
        print("Received data:", result)
        if result == "ratelimit_osuweb":
            self.notification.title = "osu!papamobil"
            self.notification.message = "You are being rate-limited by the osu! website"
            self.notification.audio = resource_path("notifysound.wav")
            self.notification.send()
            isratelimit = True
            return
        elif result == "ratelimit_api":
            self.notification.title = "osu!papamobil"
            self.notification.message = "You are being rate-limited by the API"
            self.notification.audio = resource_path("notifysound.wav")
            self.notification.send()
            isratelimit = True
            return
        if result != self.dataold and self.dataold is not None:
            isratelimit = False
            self.notification.title = "osu!papamobil"
            self.notification.message = f"{result} has been released! Check it out!"
            self.notification.audio = resource_path("notifysound.wav")
            self.notification.send()
        self.dataold = result


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
