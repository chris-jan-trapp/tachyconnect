from PyQt5.QtCore import pyqtSignal, QObject


class ReplyHandler(QObject):
    caught_reply = pyqtSignal()
    fall_back_signal = pyqtSignal(tuple)
    has_fall_back = False
    slots = {}

    def __init__(self, fall_back = None) -> None:
        super().__init__()
        if fall_back:
            self.fall_back_signal.connect(fall_back)
            self.has_fall_back = True
    
    def register_command(self, command_class, slot):
        self.slots[command_class.__name__] = slot

    def unregister_command(self, command_class):
        self.slots.pop(command_class.__name__, None)

    def handle(self, request, reply):
        print(request)
        print(reply)
        self.caught_reply.emit()
        command = request['message']
        slot = self.slots.get(command.label)
        if slot:
            slot(*reply.get_result())
            return True
        elif self.has_fall_back:
            self.fall_back_signal.emit((request, reply))
            return True
        return False