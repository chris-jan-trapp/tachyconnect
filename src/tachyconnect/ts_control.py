from time import time, sleep
from enum import Enum

from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QEventLoop, QObject, QTimer, QThread, pyqtSignal

from . import gc_constants, GSI_Parser

class CommunicationConstants:
    GSI = "GSI"
    GEOCOM = "geoCOM"
    
    GSI_MESSAGE_PREFIX = "?"
    GEOCOM_MESSAGE_PREFIX = "%R1Q"

    GEOCOM_REPLY_PREFIX = "%R1P"

    GSI_REPLY_PREFIXES = ["?", "*"]

    class ImplementationStates(Enum):
        NOT_YET_DETECTED = 0
        NOT_IMPLEMENTED = 1
        GSI = 2
        GEOCOM = 3

    COMMANDS = [
        ""
    ]


class TachyCommand(QObject):
    MESSAGE_PREFIX = ""
    REPLY_PREFIX = ""
    protocol = None
    signal = pyqtSignal

    def __init__(self, command: str, label = None, time_out = 2, signal = None, args = []) -> None:
        super().__init__()
        self.signal = signal
        self.command = command
        self.args = args
        self.transaction_id = 0
        self.time_out = time_out
        self.label = command if label is None else label
            

    def parse_reply(self, reply_bytes: bytes) -> str:
        return reply_bytes.decode('ascii')
    
    def set_transaction_id(self, id: int) -> None:
        self.transaction_id = id
    
    def get_transaction_id(self) -> int:
        return self.transaction_id

    def get_protocol(self):
        return self.protocol
    
    def __str__(self):
        try:
            return f"{self.protocol}: {self.command}, {str(self.args)}"
        except ValueError:
            return "Unitialized command object"


class GSICommand(TachyCommand):
    def __init__(self, command: str, label = None, time_out = 2, args = []) -> None:
        super().__init__(command, label, time_out=time_out, args=args)
        self.protocol=CommunicationConstants.GSI

    def get_transaction_id(self) -> int:
        return 1

    @property
    def bytes(self):
        params = ""
        if len(self.args):
            for arg in self.args:
                params += (str(arg) + " ")

        message = f"{self.command}{params}{gc_constants.CRLF}"
        return message.encode('ascii')
 

class GeoCOMCommand(TachyCommand):
    MESSAGE_PREFIX = CommunicationConstants.GEOCOM_MESSAGE_PREFIX

    def __init__(self, command: str, label = None, time_out = 2, signal = None, args = []) -> None:
        super().__init__(command, label, time_out=time_out, signal=signal, args = args)
        self.protocol=CommunicationConstants.GEOCOM

    @property
    def bytes(self):
        message = f"{self.MESSAGE_PREFIX},{str(self.command)},{self.transaction_id}:{gc_constants.CRLF}"
        return message.encode('ascii')


class TachyReply:
    def __init__(self, bites: bytes) -> None:
        self.bites = bites
        self.ascii = bites.data().decode('ascii')
        
    def __str__(self) -> str:
        return self.ascii
    
    def get_transaction_id(self) -> int:
        raise ValueError("This base type is not supposed to have an id.")

    def get_protocol(self) -> str:
        if self.ascii[0] in CommunicationConstants.GSI_REPLY_PREFIXES:
            return CommunicationConstants.GSI
        if self.ascii.startswith(CommunicationConstants.GEOCOM_REPLY_PREFIX) or self.ascii[:4] == "@W127":
            return CommunicationConstants.GEOCOM
        raise ValueError(f"Tachymeter reply uses unknown protocoll: {self.ascii}")
    
    def get_result(self):
        raise NotImplemented("Has to be implemented for each subclass.")

    def success(self):
        return False


class GSIReply(TachyReply):
    @property
    def PREFIX(self):
        self.ascii[0]

    def get_transaction_id(self) -> int:
        return 1

    def success(self):
        return self.ascii.startswith(GSI_Parser.REPLY_ACK)

    def get_result(self):
        return GSI_Parser.parse(self.ascii)
        

class GeoCOMReply(TachyReply):
    PREFIX = CommunicationConstants.GEOCOM_REPLY_PREFIX

    def get_transaction_id(self) -> int:
        header = self.ascii.split(':')[0]
        segments = header.split(",")
        return int(segments[2])

    def success(self):
        return self.ascii.startswith(GeoCOMReply.PREFIX)

    def get_result(self):
        payload = self.ascii.split(':')[1].strip()
        return payload.split(",")


class MessageQueue(QObject):
    non_requested_data = pyqtSignal(str) 
    def __init__(self, n_slots=7):
        super().__init__()
        self.indices = list(range(1, n_slots + 1))
        self.slots = {}
        self.serial = QSerialPort

    def set_serial(self, serial):
        self.serial = serial

    def append(self, msg: TachyCommand) -> int:
        def first_free_slot() -> int:
            for i in self.indices:
                if i not in self.slots.keys():
                    return i
            return False
        if self.serial is None:
            return False
        slot = first_free_slot()
        if slot and self.serial:
            self.slots[slot] = {"message": msg,
                                "timeout": time() + msg.time_out}
            msg.set_transaction_id(slot)
            self.serial.write(msg.bytes)
        return slot

    def check_timeouts(self):
        over_ripes = list(filter(lambda i: i[1]['timeout'] < time(), self.slots.items()))
        messages = []
        for index, msg in over_ripes:
            messages.append((index, self.slots.pop(index)['message']))
        return messages

    def register_reply(self, reply: TachyReply) -> tuple:
        message_id = reply.get_transaction_id()
        try:
            request = self.slots.pop(message_id)
            return request, reply
        except KeyError:
            self.non_requested_data.emit(reply.ascii)

    def close(self):
        self.serial.close()

    def __str__(self) -> str:
        n_slots = self.indices[-1]
        return f"Message queue with {n_slots} slot{'s' if n_slots > 1 else ''}"


class Dispatcher(QThread):
    pollingInterval = 1000
    serial_disconnected = pyqtSignal(str) 
    timed_out = pyqtSignal(str)
    log = pyqtSignal(str)
    non_requested_data = pyqtSignal(str)

    def __init__(self, gsi_queue: MessageQueue, geocom_queue: MessageQueue, reply_handler, parent = None) -> None:
        super(self.__class__, self).__init__(parent)
        self.pollingTimer = QTimer(self)
        self.pollingTimer.timeout.connect(self.poll)
        self.serial = QSerialPort()
        self.queues = {CommunicationConstants.GSI: gsi_queue,
                       CommunicationConstants.GEOCOM: geocom_queue}
        self.reply_types = {CommunicationConstants.GSI: GSIReply,
                            CommunicationConstants.GEOCOM: GeoCOMReply}
        self.reply_handler = reply_handler
        for queue in self.queues.values():
            queue.non_requested_data.connect(self.emit_non_requested_data)

    def emit_non_requested_data(self, data):
        self.non_requested_data.emit(data)

    def hook_up(self):
        # close port if connection is established
        self.log.emit("Connection attempt")
        if self.serial.isOpen():
            port_name = self.serial.portName
            self.serial.close()
            self.serial_disconnected.emit(port_name)
            return
        port_names = [port.portName() for port in QSerialPortInfo.availablePorts()]
        for port_name in port_names:
            ping = Ping(port_name, timeout=500)
            ping.found_tachy.connect(self.set_serial_port)
            ping.found_something.connect(self.send_log)
            ping.timed_out.connect(self.send_log)
            ping.pinging.connect(self.send_log)
            ping.fire()
    
    def start(self):
        self.pollingTimer.start(self.pollingInterval)
        loop = QEventLoop()
        loop.exec_()
        self.log.emit("Started listening.")

    def stop(self):
        self.pollingTimer.stop()

    def send_log(self, *args):
        self.log.emit(str(args))

    def set_serial_port(self, port_name):
        if self.serial.isOpen():
            self.serial.close()
        self.serial.setPortName(port_name)
        self.serial.open(QSerialPort.ReadWrite)
        for queue in self.queues.values():
            self.log.emit(f"Connecting {str(queue)} to {self.serial.portName()}")
            queue.set_serial(self.serial)
        self.start()

    def poll(self):
        if self.serial.error() == QSerialPort.ResourceError:  # device is unexpectedly removed from the system
            self.serial.close()
            self.serial_disconnected.emit(f"Connection {self.serial.portName} failed")
        if self.serial.canReadLine():
            reply = TachyReply(self.serial.readLine())
            self.register_reply(reply)
        else:
            pass
        timed_out = [q.check_timeouts() for q in self.queues.values()]
        if any(timed_out):
            description = f"Timed out: {str(list(timed_out))}"
            self.timed_out.emit(description)

    def send(self, message: TachyCommand) -> bool:
        queue = self.queues[message.protocol]
        success = queue.append(message)
        return bool(success)

    def register_reply(self, reply: TachyReply) -> tuple:
        protocol = reply.get_protocol()
        reply_type = self.reply_types[protocol]
        queue = self.queues[protocol]
        try:
            self.reply_handler.handle(*queue.register_reply(reply_type(reply.bites)))
        except TypeError:
            """TypeErrors usually stem from incoming data that can not be
            associated with any request. These are handled by the 'non_requested_data'
            signal."""
            pass
    
class Ping(QThread):
    found_tachy = pyqtSignal(str)
    found_something = pyqtSignal(str)
    timed_out = pyqtSignal(str)
    pinging = pyqtSignal(str)

    def __init__(self, port_name, timeout=1200):
        super().__init__()
        self.timeout = timeout
        self.serial = QSerialPort()
        self.serial.setPortName(port_name)
        self.serial.open(QSerialPort.ReadWrite)
        message = f"{GeoCOMCommand.MESSAGE_PREFIX},{str(gc_constants.BMM_BeepAlarm)},1:{gc_constants.CRLF}"
        self.serial.writeData(message.encode('ascii'))
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.read)

    def fire(self):
        self.timer.start(self.timeout)
        loop = QEventLoop()
        loop.exec_()
        
    def read(self):
        self.pinging.emit(f"Pinging {self.serial.portName()}")
        if self.serial.canReadLine():
            reply = bytes(self.serial.readLine()).decode('ascii')
            self.serial.close()
            if reply.startswith(GeoCOMReply.PREFIX):
                self.found_tachy.emit(self.serial.portName())
            else:
                self.found_something.emit(self.serial.portName())
        else:
            self.timed_out.emit(f"Ping timed out: {self.serial.portName()}")

        self.serial.close()
        self.quit()

