from datetime import datetime as dt
from . import gc_constants as gc
from .ts_control import GeoCOMCommand, GSICommand, CommunicationConstants
from PyQt5.QtCore import QObject

class TachyRequest(QObject):
    gsi_command = ""
    gc_command = ""
    unpacking_keys = {}
    defaults = []
    description = ""

    def __init__(self, time_out = 2, args = []):
        super().__init__()
        self.gc_command = str(gc.COMMAND_CODES.get(self.get_class_name()))
        self.time_out = time_out
        self.args = args

    def get_class_name(self):
        return self.__class__.__name__

    def __str__(self):
        return f"{self.get_class_name()}: {', '.join(self.args) if len(self.args) else 'No args'}, {self.time_out} seconds"

    def get_gsi_command(self):
        if self.gsi_command == "":
            raise NotImplementedError(f'No GSI command for {self.get_class_name()}')
        return GSICommand(self.gsi_command, self.get_class_name(), self.time_out, *self.args)

    def get_geocom_command(self):
        return GeoCOMCommand(self.gc_command, self.get_class_name(), self.time_out, *self.args)

    @classmethod
    def get_defaults(cls):
        return cls.defaults

    @classmethod
    def get_helptext(cls, i):
        if i < len(cls.helptexts):
            return cls.helptexts[i]
        else:
            return ''


class COM_NullProc(TachyRequest):
    description = """Check Communication
This function does not provide any functionality except of checking if the
communication is up and running."""


class COM_Local(TachyRequest):
    description = """Switch TPS1100 into Local Mode
Leaves on-line mode and switches TPS1100 into local mode. If in local
mode, no communication will take place. Any attempt of sending data will
be ignored. Changing local into online mode can be done manually only."""


class COM_SetDoublePrecision(TachyRequest):
    description = """Set Double Precision Setting
This function sets the precision - number of digits to the right of the
decimal - when double floating-point values are transmitted. The TPS’
system software always calculates with highest possible precision. The
default precision is fifteen digits. However, if this precision is not needed
then transmission of double data (ASCII transmission) can be speeded up
by choosing a lower precision. Especially when many double values are
transmitted this may enhance the operational speed. The usage of this
function is only meaningful if the communication is set to ASCII
transmission mode. In the case of an ASCII request, the precision of the
server side will be set. Notice that trailing Zeros will not be sent by the
server and values may be rounded. E.g. if precision is set to 3 and the exact
value is 1.99975 the resulting value will be 2.0
Note: With this function one can decrease the accuracy of the delivered
values."""
    defaults = ["15"]
    helptexts = ["Number of digits right to the comma"]


class COM_GetDoublePrecision(TachyRequest):
    description = """Get Double Precision Setting
This function returns the precision - number of digits to the right of the
decimal point - when double floating-point values are transmitted. The
usage of this function is only meaningful if the communication is set to
ASCII transmission mode. Precision is equal in both transmission
directions. In the case of an ASCII request, the precision of the server side
will be returned."""


class COM_SetSendDelay(TachyRequest):
    description = """Set Reply Delay
The GeoCOM implementation of the server has been optimised for speed.
If the server reacts to fast, then it may happen, that the client is not able to
receive the reply (complete and) correctly. This RPC inserts a delay before
the server responds to a request. This might be of interest especially for
radio data links. Reset to no delay can be done with nSendDelay = 0."""
    defaults = ["0"]
    helptexts = ["Time of transmission delay in milliseconds"]


class COM_GetBinaryAvailable(TachyRequest):
    description = """Get Binary Attribute of Server
This function gets the ability information about the server to handle binary
communication. Since TPS1100 Release 2.00 the client may make requests in
binary format which speeds up the communication by about 40-50%."""


class COM_SetBinaryAvailable(TachyRequest):
    description = """Set Binary Attribute of Server
This function sets the ability of the server to handle binary communication.
With this function, one can force to communicate in ASCII only. During
initialisation, the client checks if binary communication is enabled /
possible or not which depends on this flag. Binary data format is not
supported yet in GeoCOM Versions below 2.0."""
    defaults = [gc.BOOLEAN_TYPE.TRUE]
    helptexts = ["""TRUE: enable binary operation.
FALSE: enable ASCII operation only."""]


class COM_GetSWVersion(TachyRequest):
    gsi_command = "GET/I/WI593;"
    description = """Retrieve Server Release Information
This function retrieves the current GeoCOM release (release, version and
subversion) of the server."""


class COM_SwitchOnTPS(TachyRequest):
    gsi_command = "a"
    description = """Switch on TPS instrument
This function switches on the TPS1100 instrument and put it into remote
mode. It can also be used to switch from sleep into remote mode."""
    defaults = [gc.COM_TPS_STARTUP_MODE.COM_TPS_STARTUP_REMOTE]
    helptexts = """Run mode - use COM_TPS_STARTUP_REMOTE only!
COM_TPS_STARTUP_LOCAL will yield to erroneous behaviour."""


class COM_SwitchOffTPS(TachyRequest):
    gsi_command = "b"
    description = """Switch off TPS1100 or Set Sleep Mode
This function switches off the TPS1100 instrument or put it into sleep
mode."""
    defaults = [gc.COM_TPS_STOP_MODE.COM_TPS_STOP_SLEEP]
    helptexts = ["Stop mode"]


class COM_EnableSignOff(TachyRequest):
    description = """Enable Remote Mode Logging
This function enables logging if the Remote mode changes. See also
section 3.5 TPS1100 Instrument Modes of Operation for further
explanations."""
    defaults = [gc.BOOLEAN_TYPE.FALSE]
    helptexts = ["TRUE: enable mode logging"]


class EDM_Laserpointer(TachyRequest):
    description = """Switch on/off laserpointer
Laserpointer is only available in theodolites which supports distance
measurement without reflector."""
    defaults=[gc.ON_OFF_TYPE.ON]
    helptexts=["""
ON - switch Laserpointer on
OFF - switch Laserpointer off"""]


class EDM_SetBumerang(TachyRequest):
    description = """Switch boomerang filter on/off
The boomerang filter is not available for some add-on EDM’s.
Deleted in TPS1100"""
    defaults = [gc.ON_OFF_TYPE.OFF]
    helptexts = ["""ON - switch boomerang filter on
OFF - switch boomerang filter off"""]


class EDM_On(TachyRequest):
    description = """Switch on/off EDM
Normal distance measurement switches on or off the EDM automatically. If
there is no supply voltage for the EDM, EDM_On also connects it. Normally
the supply voltage is switched off together with the EDM, unless the
Tracklight or the diode laser is switched on too, or the permanent power-on-
mode is set. These functions overlie the functionality of EDM_On and EDM
cannot be switched off before the Tracklight or the diode laser stops
working. However, after 10 min the EDM will be switched off.
Deleted in TPS1100"""
    defaults=[gc.ON_OFF_TYPE.ON]
    helptexts=["""ON - switch EDM on
OFF - switch EDM off"""]


class EDM_SetTrkLightSwitch(TachyRequest):
    description = """Switch on/off tracklight
The Tracklight must be available for EDM.
Replaced by: EDM_SetEGLIntensity in TPS1100"""
    defaults=[gc.ON_OFF_TYPE.ON]
    helptexts=["""ON - switch on Tracklight
OFF - switch off Tracklight"""]


class EDM_SetTrkLightBrightness(TachyRequest):
    description = """Change intensity of tracklight
The Tracklight must be available for EDM.
Replaced by: EDM_SetEGLIntensity in TPS1100"""
    defaults=[gc.EDM_TRKLIGHT_BRIGHTNESS.EDM_HIGH_BRIGHTNESS]
    helptexts=[""""""]


class EDM_GetTrkLightSwitch(TachyRequest):
    description = """Get status of tracklight switch
The Tracklight must be available for EDM.
Replaced by: EDM_GetEGLIntensity in TPS1100"""


class EDM_GetTrkLightBrightness(TachyRequest):
    description = """Get value of intensity of tracklight
The Tracklight must be available for EDM.
Replaced by: EDM_GetEGLIntensity"""


class EDM_GetBumerang(TachyRequest):
    description = """Get status of boomerang filter
Call this function to retrieve the status of the "boomerang filter" (i.e. ON,
OFF). If the distance is within 60-100 meters and the boomerang filter is
turned off, wrong measurement results are possible. With the boomerang
filter turned on, the measurement accuracy can be increased until up to max.
2.5 cm.
The boomerang filter is not available for some add-on EDM’s.
Deleted in TPS1100"""


class EDM_GetEglIntensity(TachyRequest):
    description = """Get value of intensity of guide light
The Electronic Guide Light must be implemented in the theodolite."""


class EDM_SetEglIntensity(TachyRequest):
    description = """Change intensity of guide light
The Electronic Guide Light must be implemented in the theodolite.
New since TPS1100"""
    defaults=[gc.EDM_EGLINTENSITY_TYPE.EDM_EGLINTEN_HIGH]
    helptexts=[""""""]


class TMC_GetAngle1(TachyRequest):
    description = """Returns complete angle measurement
This function carries out an angle measurement and, in dependence of
configuration, inclination measurement and returns the results. As shown
the result is very comprehensive. For simple angle measurements use
TMC_GetAngle5 or TMC_GetSimpleMea instead."""
    defaults=[gc.TMC_INCLINE_PRG.TMC_AUTO_INC]
    helptexts=["Inclination sensor measurement mode."]


class TMC_SetInclineSwitch(TachyRequest):
    description = """Switch dual axis compensator on or off
This function switches the dual axis compensator on or off."""
    defaults=[gc.ON_OFF_TYPE.ON]
    helptexts=["Dual axis compensator's state."]


class TMC_GetInclineSwitch(TachyRequest):
    description = """Get the dual axis compensator's state
This function returns the current dual axis compensator's state."""


class TMC_DoMeasure(TachyRequest):
    description = """Carries out a distance measurement
This function carries out a distance measurement in a variety of TMC
measurement modes like single distance, rapid tracking,... . Please note that
this command does not output any values (distances). In order to get the
values you have to use other measurement functions such as
TMC_GetCoordinate, TMC_GetSimpleMea or TMC_GetAngle.
The value of the distance measured is kept in the instrument up to the next
TMC_DoMeasure command where a new distance is requested or the
distance is clear by the measurement program TMC_CLEAR.
Note: If you perform a distance measurement with the measure program
TMC_DEF_DIST, the distance sensor will be work with the set EDM
mode, see TMC_SetEdmMode."""
    defaults = [gc.TMC_MEASURE_PRG.TMC_DO_MEASURE, gc.TMC_INCLINE_PRG.TMC_AUTO_INC]
    helptexts = ["TMC measurement mode.", "Inclination sensor measurement mode."]


class TMC_GetStation(TachyRequest):
    description = """Get the coordinates of the instrument station
This function is used to get the co-ordinates of the instrument station."""


class TMC_SetStation(TachyRequest):
    description = """Set the coordinates of the instrument station
This function is used to set the co-ordinates of the instrument station."""
    defaults = ["0", "0", "0", "0"]
    helptexts = ["E0[double] - Station easting coordinate",
               "N0[double] - Station northing coordinate",
               "H0[double] - Station height coordinate",
               "Hi[double] - Instrument height"]


class TMC_GetHeight(TachyRequest):
    gsi_command = "GET/I/WI88"
    description = """"Returns the current reflector height
This function returns the current reflector height."""



class TMC_SetHeight(TachyRequest):
    description = """Sets new reflector height
This function sets a new reflector height."""
    defaults=["0"]
    helptexts=["New reflector height"]


class TMC_GetAngSwitch(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_SetAngSwitch(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_SetHandDist(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_SetEdmMode(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_GetEdmMode(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_GetSignal(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_GetPrismCorr(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_SetPrismCorr(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_GetFace(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_SetAtmCorr(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_GetAtmCorr(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_SetRefractiveCorr(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_GetRefractiveCorr(TachyRequest):
    gsi_command = "GET/I/WI538"


class TMC_GetCoordinate(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_GetCoordinate1(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_SetRefractiveMethod(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_GetRefractiveMethod(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_GetAngle5(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_GetSimpleMea(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_SetOrientation(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_IfDataAzeCorrError(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_IfDataIncCorrError(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_GetSimpleCoord(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_QuickDist(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class TMC_GetSlopeDistCorr(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class CSV_GetInstrumentNo(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class CSV_GetInstrumentName(TachyRequest):
    gsi_command = "GET/I/WI13"


class CSV_SetUserInstrumentName(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class CSV_GetUserInstrumentName(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class CSV_SetDateTime(TachyRequest):
    helptexts = ["Year", "Month", "Day", "Hour", "Minute", "Second"]
    #args_widget = "QLineEdit"

    @classmethod
    def get_defaults(cls):
        return dt.now().strftime("%Y,%m,%d,%H,%M,%S").split(",")

class CSV_GetDateTime(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class CSV_GetVBat(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class CSV_GetVMem(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class CSV_GetIntTemp(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class CSV_GetSWVersion(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class CSV_GetSWVersion2(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class CSV_GetDeviceConfig(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class MOT_StartController(TachyRequest):
    description = """Start motor controller
This command is used to enable remote or user interaction to the motor
controller."""
    defaults=[gc.MOT_MODE.MOT_MANUPOS]
    helptexts=["""Controller mode. If used together with
MOT_SetVelocity the control mode has
to be MOT_OCONST"""]


class MOT_StopController(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class MOT_SetVelocity(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class MOT_ReadLockStatus(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class WIR_GetRecFormat(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class WIR_SetRecFormat(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_SetTol(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_ReadTol(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_SetTimeout(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_ReadTimeout(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_LockIn(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_SetATRStatus(TachyRequest):
    description = ""
    defaults = [gc.ON_OFF_TYPE.ON]
    helptexts = ['On or off']


class AUT_GetATRStatus(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_SetLockStatus(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_GetLockStatus(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_MakePositioning(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_MakePositioning4(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_ChangeFace(TachyRequest):
    description = """"""
    defaults = [gc.AUT_POSMODE.AUT_NORMAL,
                gc.AUT_ATRMODE.AUT_TARGET,
                gc.BOOLEAN_TYPE.FALSE]
    helptexts = ["""\
Position mode:
AUT_NORMAL: uses the current value of the compensator.
For values >25GON positioning might tend to inexact.
AUT_PRECISE: tries to measure exact inclination of target.
Tends to long position time
(check AUT_TIMEOUT and/or COM-time out if necessary).""",
"""Mode of ATR:
AUT_POSITION: conventional position to other face.
AUT_TARGET: tries to position onto a target in the destination area.
This set is only possible if ATR exists and is activated.""",
"""It’s reserved for future use, set bDummy always to FALSE"""]


class AUT_ChangeFace4(AUT_ChangeFace):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_Search(TachyRequest):
    description = """"""
    defaults=["0.1", "0.3"]
    helptexts=["Horizontal search angle in rad.",
               "Vertical search angle in rad."]


class AUT_Search2(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_GetFineAdjustMode(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_SetFineAdjustMode(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_FineAdjust(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_FineAdjust3(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_GetUserSpiral(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_SetUserSpiral(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_GetSearchArea(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_SetSearchArea(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_PS_SetRange(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_PS_EnableRange(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUT_PS_SearchNext(TachyRequest):
    description = """Searching for the next target
This command executes the 360º default PowerSearch and searches for the next target. A previously defined
PowerSearch window (AUT_SetSearchArea) is not taken into account. Use AUT_PS_SearchWindow to do so.
TPS1200+"""
    defaults=[gc.AUT_DIRECTION.AUT_ANTICLOCKWISE, gc.BOOLEAN_TYPE.TRUE]
    helptexts=["Defines the searching direction (CLKW=1 or ACLKW=-1)", """TRUE: Searching starts -10 gon to the given direction
lDirection. This setting finds targets left of the telescope
direction faster"""]


class AUT_PS_SearchWindow(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class BMM_BeepOn(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class BMM_BeepOff(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class BMM_BeepNormal(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class BMM_BeepAlarm(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class CTL_GetUpCounter(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class SUP_GetConfig(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class SUP_SetConfig(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class SUP_SwitchLowTempControl(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class BAP_GetLastDisplayedError(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class BAP_SetPrismType(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class BAP_GetPrismType(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class BAP_MeasDistanceAngle(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class BAP_GetMeasPrg(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class BAP_SetMeasPrg(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class BAP_SearchTarget(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class BAP_SetTargetType(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class BAP_GetTargetType(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class BAP_GetPrismDef(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class BAP_SetPrismDef(TachyRequest):
    description = """"""
    defaults=[""""""]
    helptexts=[""""""]


class AUS_GetUserAtrState(TachyRequest):
    description = """Get the status of the ATR mode
Get the current status of the ATR mode on TCA instruments. This
command does not indicate whether the ATR has currently acquired a
prism. It replaces the function AUT_GetAtrStatus."""


class AUS_SetUserAtrState(TachyRequest):
    description = """Set the status of the ATR mode
Activate respectively deactivate the ATR mode.
Activate ATR mode:
The ATR mode is activated and the LOCK mode (if sets) will be reset
automatically also."""
    defaults = [gc.ON_OFF_TYPE.OFF]
    helptexts = ["State of the ATR mode"]


class AUS_GetUserLockState(TachyRequest):
    description = """Get the status of the lock switch
This command gets the current LOCK switch. This command is valid for
TCA instruments only and does not indicate whether the ATR has a prism
in lock or not.
With the function MOT_ReadLockStatus you can find out whether a
target is locked or not.
This command is valid for TCA instruments only. It replaces the function
AUT_GetLockStatu"""


class AUS_SetUserLockState(TachyRequest):
    description = """Set the lock status.
Status ON:
The target tracking functionality is available but not activated. In order to
activate target tracking, see the function AUT_LockIn. The ATR mode will
be set automatically.
Status OFF:
A running target tracking will be aborted and the manual driving wheel is
activated. The ATR mode will be not reset automatically respectively keep
unchanged.
This command is valid for TCA instruments only. It replaces the function
AUT_SetLockStatus."""
    defaults = [gc.ON_OFF_TYPE.OFF]
    helptexts = ["State of the ATR lock switch"]


class AUS_SwitchRcsSearch(TachyRequest):
    description = """Set the RCS searching mode switch.
If the RCS style searching is enabled, then the extended for
BAP_SearchTarget or after a loss of lock is activated.
This command is valid for TCA instruments only."""
    defaults = [gc.ON_OFF_TYPE.OFF]
    helptexts = ["Get RCS-Searching mode switch"]


class AUS_GetRcsSearchSwitch(TachyRequest):
    description = """Get RCS-Searching mode switch
This command gets the current RCS-Searching mode switch.
If RCS style searching is enabled, then the extended searching for
BAP_SearchTarget or after a loss of lock is activated.
This command is valid for TCA instruments only."""


class IOS_BeepOn(TachyRequest):
    description = """Start a beep-signal
This function switches on the beep-signal with the intensity nIntens. If a
continuous signal is active, it will be stopped first. Turn off the beeping
device with IOS_BeepOff"""
    defaults = ["100"]
    helptexts = ["""Intensity of the beep-signal (volume)
expressed as a percentage.
Default value is 100 %"""]


class IOS_BeepOff(TachyRequest):
    description = """Stop active beep-signal
This function switches off the beep-signal."""


ALL_COMMANDS = [
    COM_NullProc,
    COM_Local,
    COM_SetDoublePrecision,
    COM_GetDoublePrecision,
    COM_SetSendDelay,
    COM_GetSWVersion,
    COM_SwitchOnTPS,
    COM_SwitchOffTPS,
    COM_GetBinaryAvailable,
    COM_SetBinaryAvailable,
    COM_EnableSignOff,
    EDM_Laserpointer,
    EDM_SetBumerang,
    EDM_On,
    EDM_SetTrkLightSwitch,
    EDM_SetTrkLightBrightness,
    EDM_GetTrkLightSwitch,
    EDM_GetTrkLightBrightness,
    EDM_GetBumerang,
    EDM_GetEglIntensity,
    EDM_SetEglIntensity,
    TMC_GetAngle1,
    TMC_SetInclineSwitch,
    TMC_GetInclineSwitch,
    TMC_DoMeasure,
    TMC_GetStation,
    TMC_SetStation,
    TMC_GetHeight,
    TMC_SetHeight,
    TMC_GetAngSwitch,
    TMC_SetAngSwitch,
    TMC_SetHandDist,
    TMC_SetEdmMode,
    TMC_GetEdmMode,
    TMC_GetSignal,
    TMC_GetPrismCorr,
    TMC_SetPrismCorr,
    TMC_GetFace,
    TMC_SetAtmCorr,
    TMC_GetAtmCorr,
    TMC_SetRefractiveCorr,
    TMC_GetRefractiveCorr,
    TMC_GetCoordinate,
    TMC_GetCoordinate1,
    TMC_SetRefractiveMethod,
    TMC_GetRefractiveMethod,
    TMC_GetAngle5,
    TMC_GetSimpleMea,
    TMC_SetOrientation,
    TMC_IfDataAzeCorrError,
    TMC_IfDataIncCorrError,
    TMC_GetSimpleCoord,
    TMC_QuickDist,
    TMC_GetSlopeDistCorr,
    CSV_GetInstrumentNo,
    CSV_GetInstrumentName,
    CSV_SetUserInstrumentName,
    CSV_GetUserInstrumentName,
    CSV_SetDateTime,
    CSV_GetDateTime,
    CSV_GetVBat,
    CSV_GetVMem,
    CSV_GetIntTemp,
    CSV_GetSWVersion,
    CSV_GetSWVersion2,
    CSV_GetDeviceConfig,
    MOT_StartController,
    MOT_StopController,
    MOT_SetVelocity,
    MOT_ReadLockStatus,
    WIR_GetRecFormat,
    WIR_SetRecFormat,
    AUT_SetTol,
    AUT_ReadTol,
    AUT_SetTimeout,
    AUT_ReadTimeout,
    AUT_LockIn,
    AUT_SetATRStatus,
    AUT_GetATRStatus,
    AUT_SetLockStatus,
    AUT_GetLockStatus,
    AUT_MakePositioning,
    AUT_MakePositioning4,
    AUT_ChangeFace,
    AUT_ChangeFace4,
    AUT_Search,
    AUT_Search2,
    AUT_GetFineAdjustMode,
    AUT_SetFineAdjustMode,
    AUT_FineAdjust,
    AUT_FineAdjust3,
    AUT_GetUserSpiral,
    AUT_SetUserSpiral,
    AUT_GetSearchArea,
    AUT_SetSearchArea,
    AUT_PS_SetRange,
    AUT_PS_EnableRange,
    AUT_PS_SearchNext,
    AUT_PS_SearchWindow,
    BMM_BeepOn,
    BMM_BeepOff,
    BMM_BeepNormal,
    BMM_BeepAlarm,
    CTL_GetUpCounter,
    SUP_GetConfig,
    SUP_SetConfig,
    SUP_SwitchLowTempControl,
    BAP_GetLastDisplayedError,
    BAP_SetPrismType,
    BAP_GetPrismType,
    BAP_MeasDistanceAngle,
    BAP_GetMeasPrg,
    BAP_SetMeasPrg,
    BAP_SearchTarget,
    BAP_SetTargetType,
    BAP_GetTargetType,
    BAP_GetPrismDef,
    BAP_SetPrismDef,
    AUS_SetUserAtrState,
    AUS_GetUserAtrState,
    AUS_SetUserLockState,
    AUS_GetUserLockState,
    AUS_SwitchRcsSearch,
    AUS_GetRcsSearchSwitch,
    IOS_BeepOff,
    IOS_BeepOn]

if __name__=="__main__":
    set_station = TMC_SetStation()
    print(f"Code for set station: {set_station.gc_command}")

