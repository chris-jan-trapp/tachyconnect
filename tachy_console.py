import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow
)
from PyQt5.QtCore import pyqtSignal
from ui.main_window import Ui_MainWindow
from Communication.ts_control import Dispatcher, MessageQueue
from Communication.ReplyHandler import ReplyHandler
from Communication import TachyRequest


class Window(QMainWindow, Ui_MainWindow):
    ready = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.reply_handler = ReplyHandler(fall_back=self.stringify)
        self.dispatcher = Dispatcher(MessageQueue(1), MessageQueue(7), self.reply_handler)
        self.connectSignalsSlots()

    
    def connectSignalsSlots(self):
        self.action_Quit.triggered.connect(self.close)
        self.send_command.clicked.connect(self.toast)
        self.actionconnect.triggered.connect(self.dispatcher.hook_up)
        self.dispatcher.timed_out.connect(self.log_append)
        self.dispatcher.log.connect(self.log_append)

    def log_append(self, text):
        self.log_viewer.setPlainText(self.log_viewer.toPlainText() + "\n" + text)
        scroll_bar = self.log_viewer.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

    def stringify(self, *args):
        self.log_append(str(args))

    def reply_received(self, request, reply):
        self.log_append(f"Received: {reply}")

    def toast(self):
        # beep = GeoCOMCommand(str(gc.BMM_BeepAlarm))
        # self.dispatcher.send(beep)
        borb = TachyRequest.TMC_GetHeight()
        self.dispatcher.send(borb.get_geocom_command())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()

    sys.exit(app.exec())