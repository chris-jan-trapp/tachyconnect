from PyQt5.QtCore import pyqtSignal, QObject

class ReplyHandler(QObject):
    fall_back_signal = pyqtSignal(tuple)
    has_fall_back = False
    slots = {}

    def __init__(self, fall_back = None) -> None:
        super().__init__()
        if fall_back:
            self.fall_back_signal.connect(fall_back)
            self.has_fall_back = True
    
    def register_command(self, command, slot):
        self.slots[command.label] = slot    

    def disconnect_all(self):
        for signal in self.signals.values():
            signal.disconnect()
        self.fall_back_signal.disconnect()

    def handle(self, request, reply):
        print(request)
        print(reply)
        command = request['message']
        slot = self.slots.get(command.label)
        if slot:
            request.signal.connect(slot)
            request.signal.emit()
            request.signal.disconnect()
        if self.has_fall_back:
            self.fall_back_signal.emit((request, reply))
            return request, reply
        return False