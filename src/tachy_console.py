from ast import arg
from enum import Enum
import sys, json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QDialog, QLineEdit, QComboBox
)
from PyQt5.QtCore import pyqtSignal
from matplotlib.pyplot import phase_spectrum
from ui.main_window import Ui_MainWindow
from tachyconnect.TachyJoystick import TachyJoystick
from tachyconnect.ts_control import Dispatcher, MessageQueue, CommunicationConstants, GeoCOMCommand
from tachyconnect.ReplyHandler import ReplyHandler
from tachyconnect import TachyRequest, gc_constants
from PyQt5.QtCore import Qt, QVariant


class Window(QMainWindow, Ui_MainWindow):
    ready = pyqtSignal()
    last_command = ""
    test_list = []
    commands_by_name = {}
    device_type = ""
    connection_attempts = 0
    connected = False
    slots = {}
    implementation_chart = {}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.reply_handler = ReplyHandler(fall_back=self.show_request_reply)
        self.reply_handler.register_command(TachyRequest.CSV_GetInstrumentName, self.identify)
        self.commands_by_name = dict(map(lambda k: (k.__name__, k), TachyRequest.ALL_COMMANDS))

        # for command in TachyRequest.ALL_COMMANDS:
        #     self.reply_handler.register_command(command, self.run_and_log)
        self.dispatcher = Dispatcher(MessageQueue(1), MessageQueue(7), self.reply_handler)
        
        self.dialect_selector.addItem(CommunicationConstants.GEOCOM)
        self.dialect_selector.addItem(CommunicationConstants.GSI)
        self.command_selector.addItems([klass.__name__ for klass in TachyRequest.ALL_COMMANDS])
        self.command_selector.activated.connect(self.add_args_widget)
        
        self.tachy_joystick_dlg = TachyJoystick(self.dispatcher, self, Qt.Dialog | Qt.Tool)
        
        self.command_args_widget = []  # array for multiple widgets
        
        self.connectSignalsSlots()
    
    # add the appropriate args widget (QComboBox / QLineEdit) when a command is selected
    def add_args_widget(self):
        # remove widget if there is one already
        if self.command_args_widget:
            for widget in self.command_args_widget:
                widget.setParent(None)
                self.horizontalLayout.removeWidget(widget)
            self.command_args_widget = []
        
        command_class = self.commands_by_name[self.command_selector.currentText()]
        self.command_selector.setToolTip(command_class.description)
        
        
        for i, default_value in enumerate(command_class.get_defaults()):
            if type(default_value) == str:
                widget = QLineEdit()
                widget.setText(default_value)
            if isinstance(default_value, Enum):
                our_enum = default_value.__class__
                widget = QComboBox()
                for j, entry in enumerate(our_enum):
                    widget.addItem(entry.name, str(entry.value))
                    
                    if entry == default_value:
                        widget.setCurrentIndex(j)
                
            widget.setToolTip(command_class.get_helptext(i))
            self.command_args_widget.append(widget)
            self.horizontalLayout.insertWidget(len(self.horizontalLayout)-1, widget)

    def connectSignalsSlots(self):
        self.action_Quit.triggered.connect(self.close)
        self.send_command.clicked.connect(self.toast)
        self.actionconnect.triggered.connect(self.dispatcher.hook_up)
        self.actionidentify.triggered.connect(self.request_id)
        self.actionextract_capabilities.triggered.connect(self.extract_capabilities)
        self.actiondump_implementation_chart.triggered.connect(self.dump_capabilities)
        self.actionJoystick.triggered.connect(self.show_joystick)
        self.dispatcher.log.connect(self.log_append)
        self.dispatcher.non_requested_data.connect(self.surprise)
        self.reply_handler.caught_reply.connect(self.log_reply)
        
    def show_joystick(self):
        self.tachy_joystick_dlg.show()

    def request_id(self):
        self.dispatcher.send(TachyRequest.CSV_GetInstrumentName().get_geocom_command())
    
    def identify(self, *results):
        print(results)
        if results[0] == str(gc_constants.GRC_OK):
            device_name = results[-1]
            self.device_type = device_name
            self.log_append(f"Found {device_name}.")
            self.statusbar.showMessage(f"Connected: {device_name}")
        
    def extract_capabilities(self):
        self.slots = dict(self.reply_handler.slots)
        self.test_list = list(TachyRequest.ALL_COMMANDS)
        for klass in TachyRequest.ALL_COMMANDS:
            self.reply_handler.register_command(klass, self.run_and_log)
        self.run_and_log()
        
    def run_and_log(self, *previous_results):
        if previous_results:
            self.implementation_chart[self.last_command.__name__] = previous_results[0] != str(gc_constants.GRC_COM_PROC_UNAVAIL)
            self.stringify(*previous_results)
        if self.test_list:
            command_class = self.test_list.pop()
            self.log_append(f"Sending {command_class.__name__}, getting:")
            self.last_command = command_class
            self.dispatcher.send(command_class().get_geocom_command())
        else:
            self.log_append("FINISHED")
            self.reply_handler.slots = self.slots
            self.dump_capabilities()

    def read_return_codes(self, verbose = False, *args):
        codes = ""
        book = gc_constants.MESSAGES if verbose else gc_constants.CODES
        for arg in args:
            try:
                key = int(arg)
            except TypeError:
                next
            codes += book.get(key, "Unknown code") + "\n"
        return codes
    
    def log_codes(self, *args):
        self.log_append(self.read_return_codes(True, *args))

    def log_append(self, text):
        self.log_viewer.setPlainText(self.log_viewer.toPlainText() + "\n" + text)
        scroll_bar = self.log_viewer.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())
    
    def log_reply(self, reply):
        self.log_append("Reply: " + str(reply))

    def undict(self, d):
        self.log_append(str(d))

    def stringify(self, *args):
        try:
            self.log_append(args[1].get_results())
        except:
            self.log_append(str(args))

    def show_request_reply(self, message_and_reply):
        message, reply = message_and_reply[:2]
        print(message, reply)
        request = message['message']
        results = reply.get_result()
        result_text = f"{gc_constants.MESSAGES[int(results.pop(0))]}{', '.join(results)}"
        text = f"""Request: {str(request)}
        returned: {str(reply)} with: {result_text}"""
        self.log_append(text)
        
    def dump_capabilities(self):
        if not self.device_type and self.implementation_chart:
            self.statusbar.showMessage("Missing capabilities or device id for dump!")
            return
        capabilities = {self.device_type: self.implementation_chart}
        file_name, filtr = QFileDialog.getSaveFileName(self, "Select File", "", "Json Files (*.json)")
        with open(file_name, 'w') as dumpfile:
            json.dump(capabilities, dumpfile, indent=2)

    def reply_received(self, request, reply):
        self.log_append(f"Received: {reply}")

    def surprise(self, tadaa):
        self.log_append("This came in unsolicited:\n" + tadaa)

    def toast(self):
        # beep = GeoCOMCommand(str(gc_constants.EDM_Laserpointer),"LAS",2,1)
        # self.dispatcher.send(beep)
        # self.test_list = list(TachyRequest.ALL_COMMANDS)
        # self.run_and_log()
        command = self.commands_by_name[self.command_selector.currentText()]
        # todo: get args from self.command_args_widget array
        #args = self.args.text().strip().split(';')
        #args = ";".join([str(widget.currentData()) for widget in self.command_args_widget])
        def get_arg_from_widget(widget):
            if isinstance(widget, QLineEdit):
                return widget.text().strip()
            if isinstance(widget, QComboBox):
                return str(widget.currentData())
        args = [get_arg_from_widget(widget) for widget in self.command_args_widget]
        print("Args: ", ";".join(args))
        # if self.dialect_selector.currentText() == CommunicationConstants.GSI:
        #     self.dispatcher.send(command(args = args).get_gsi_command())
        if self.dialect_selector.currentText() == CommunicationConstants.GEOCOM:
            self.dispatcher.send(command(args = args).get_geocom_command())
            print("Sent ascii: " + str(command(args = args).get_geocom_command()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()

    sys.exit(app.exec())