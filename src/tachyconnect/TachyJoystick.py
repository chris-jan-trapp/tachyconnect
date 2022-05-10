from ast import arg
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from ui.tachy_joystick import Ui_Dialog as Ui_TachyJoystick
from tachyconnect.ts_control import Dispatcher
from tachyconnect.TachyRequest import (MOT_StartController,
                                       MOT_StopController,
                                       MOT_SetVelocity,
                                       AUT_Search,
                                       AUT_LockIn,
                                       AUS_SetUserLockState,
                                       AUS_GetUserLockState,
                                       AUS_SetUserAtrState,
                                       EDM_SetEglIntensity
)
from tachyconnect.ReplyHandler import CommandChain

class TachyJoystick(QDialog, Ui_TachyJoystick):
    MAX_SPEED = 0.42
    STEP = 0.06
    
    LOCKED = "🔒"
    UNLOCKED = "🔓"
    LOCK_STATES = {'0': UNLOCKED,
                   '1': LOCKED}
    
    def __init__(self, dispatcher, parent=None, flags=Qt.Dialog | Qt.Tool):
        super().__init__(parent = parent, flags = flags)
        self.reject = self.accept
        self.dispatcher = dispatcher
        self.dispatcher.reply_handler.register_command(AUT_Search, self.searched)
        self.dispatcher.reply_handler.register_command(AUS_GetUserLockState, self.show_lock_state)
        self.hzSpeed = 0
        self.vtSpeed = 0
        self.setupUi(self)
        self.connectSignalsSlots()
        
    def searched(self, *args):
        print(args)
        if args[0] == '0':
            chain = CommandChain(self.dispatcher)
            chain.set_commands([AUS_SetUserAtrState, 1 , ['1']],
                               [AUS_SetUserLockState, 1, ['1']],
                               [AUT_LockIn, 2, []]
                               )
            chain.run_chain
            # self.dispatcher.send(AUS_SetUserAtrState(args=['1']).get_geocom_command())
            # self.dispatcher.send(AUS_SetUserLockState(args=['1']).get_geocom_command())
            # self.dispatcher.send(AUT_LockIn().get_geocom_command())
            self.get_lock_state()
    
    def get_lock_state(self):
        self.dispatcher.send(AUS_GetUserLockState().get_geocom_command())
    
    def show_lock_state(self, *args):
        print('Lock state: ' + args)
        if args[0] == '0':
            self.lockState.setText(TachyJoystick.LOCK_STATES[args[-1]])
    
    def connectSignalsSlots(self):
        self.joystickUp.clicked.connect(self.up)
        self.joystickOk.clicked.connect(self.accept)
        self.joystickDown.clicked.connect(self.down)
        self.joystickStop.clicked.connect(self.stop)
        self.joystickLeft.clicked.connect(self.left)
        self.joystickRight.clicked.connect(self.right)
        self.joystickLock.clicked.connect(self.lock)
        
    def lock(self):
        self.get_lock_state()
        self.dispatcher.send(AUT_Search(time_out=8,args=[.1, .3]).get_geocom_command())
    
    def lights_off(self):
        self.dispatcher.send(EDM_SetEglIntensity(args=['0']).get_geocom_command())
    
    def show(self):
        super().show()
        self.dispatcher.send(MOT_StartController(args=['1']).get_geocom_command())
        self.dispatcher.send(EDM_SetEglIntensity(args=['3']).get_geocom_command())
        self.get_lock_state()
        
    
    def accept(self):
        self.stop()
        self.dispatcher.send(MOT_StopController().get_geocom_command())
        self.lights_off()
        super().accept()
    
    def set_velocity(self):
        self.dispatcher.send(MOT_SetVelocity(args=[self.hzSpeed, self.vtSpeed]).get_geocom_command())
    
    def up(self):
        if abs(self.vtSpeed) < TachyJoystick.MAX_SPEED:
            self.vtSpeed -= TachyJoystick.STEP
            self.set_velocity()
    
    def down(self):
        if abs(self.vtSpeed) < TachyJoystick.MAX_SPEED:
            self.vtSpeed += TachyJoystick.STEP
            self.set_velocity()

    def left(self):
        if abs(self.hzSpeed) < TachyJoystick.MAX_SPEED:
            self.hzSpeed += TachyJoystick.STEP
            self.set_velocity()

    def right(self):
        if abs(self.hzSpeed) < TachyJoystick.MAX_SPEED:
            self.hzSpeed -= TachyJoystick.STEP
            self.set_velocity()

    def stop(self):
        self.hzSpeed = self.vtSpeed = 0
        self.set_velocity()
        