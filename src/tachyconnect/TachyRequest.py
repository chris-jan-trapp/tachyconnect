from . import gc_constants as gc
from .ts_control import GeoCOMCommand, GSICommand, CommunicationConstants
from PyQt5.QtCore import QObject, pyqtSignal

class TachyRequest(QObject):
    gsi_command = ""
    gc_command = ""
    unpacking_keys = {}
    signal = pyqtSignal(QObject)

    def __init__(self, time_out = 2, args = []) -> None:
        super().__init__()
        self.gc_command = str(gc.COMMAND_CODES.get(self.get_class_name()))
        self.time_out = time_out
        self.args = args

    def get_class_name(self):
        return self.__class__.__name__

    def __str__(self) -> str:
        return f"{self.get_class_name()}: {', '.join(self.args) if len(self.args) else 'No args'}, {self.time_out} seconds"

    def get_gsi_command(self):
        if self.gsi_command == "":
            raise NotImplementedError(f'No GSI command for {self.get_class_name()}')
        return GSICommand(self.gsi_command, self.get_class_name(), self.time_out, *self.args)
    
    def get_geocom_command(self):
        return GeoCOMCommand(self.gc_command, self.get_class_name(), self.time_out, self.signal, *self.args)


class BMM_BeepAlarm(TachyRequest):
    pass


class BMM_BeepNormal(TachyRequest):
    pass


class COM_GetDoublePrecision(TachyRequest):
    pass


class COM_GetSWVersion(TachyRequest):
    pass


class COM_NullProc(TachyRequest):
    pass


class COM_SetDoublePrecision(TachyRequest):
    pass


class COM_SwitchOffTPS(TachyRequest):
    gsi_command = "b"


class COM_SwitchOnTPS(TachyRequest):
    gsi_command = "a"


class CSV_GetDateTime(TachyRequest):
    pass


class CSV_GetDeviceConfig(TachyRequest):
    pass


class CSV_GetInstrumentName(TachyRequest):
    gsi_command = "GET/I/WI13"


class CSV_GetInstrumentNo(TachyRequest):
    pass


class CSV_GetIntTemp(TachyRequest):
    pass


class CSV_GetSWVersion(TachyRequest):
    gsi_command = "GET/I/WI593;"


class CSV_SetDateTime(TachyRequest):
    pass


class EDM_GetEglIntensity(TachyRequest):
    pass


class EDM_Laserpointer(TachyRequest):
    pass


class EDM_SetEglIntensity(TachyRequest):
    pass


class SUP_GetConfig(TachyRequest):
    pass


class SUP_SetConfig(TachyRequest):
    pass


class TMC_DoMeasure(TachyRequest):
    pass


class TMC_GetAngle1(TachyRequest):
    pass


class TMC_GetAngle5(TachyRequest):
    pass


class TMC_GetAngSwitch(TachyRequest):
    pass


class TMC_GetAtmCorr(TachyRequest):
    pass


class TMC_GetCoordinate(TachyRequest):
    pass


class TMC_GetEdmMode(TachyRequest):
    pass


class TMC_GetFace(TachyRequest):
    pass


class TMC_GetHeight(TachyRequest):
    gsi_command = "GET/I/WI88"


class TMC_GetInclineSwitch(TachyRequest):
    pass


class TMC_GetPrismCorr(TachyRequest):
    pass


class TMC_GetRefractiveCorr(TachyRequest):
    gsi_command = "GET/I/WI538"


class TMC_GetRefractiveMethod(TachyRequest):
    pass


class TMC_GetSignal(TachyRequest):
    pass


class TMC_GetSimpleCoord(TachyRequest):
    pass


class TMC_GetSimpleMea(TachyRequest):
    pass


class TMC_GetSlopeDistCorr(TachyRequest):
    pass


class TMC_GetStation(TachyRequest):
    pass


class TMC_IfDataAzeCorrError(TachyRequest):
    pass


class TMC_IfDataIncCorrError(TachyRequest):
    pass


class TMC_QuickDist(TachyRequest):
    pass


class TMC_SetAngSwitch(TachyRequest):
    pass


class TMC_SetAtmCorr(TachyRequest):
    pass


class TMC_SetEdmMode(TachyRequest):
    pass


class TMC_SetHandDist(TachyRequest):
    pass


class TMC_SetHeight(TachyRequest):
    pass


class TMC_SetInclineSwitch(TachyRequest):
    pass


class TMC_SetOrientation(TachyRequest):
    pass


class TMC_SetRefractiveCorr(TachyRequest):
    pass


class TMC_SetRefractiveMethod(TachyRequest):
    pass


class TMC_SetStation(TachyRequest):
    pass

ALL_COMMANDS = [
    BMM_BeepAlarm,
    BMM_BeepNormal,
    COM_GetDoublePrecision,
    COM_GetSWVersion,
    COM_NullProc,
    COM_SetDoublePrecision,
    COM_SwitchOffTPS,
    COM_SwitchOnTPS,
    CSV_GetDateTime,
    CSV_GetDeviceConfig,
    CSV_GetInstrumentName,
    CSV_GetInstrumentNo,
    CSV_GetIntTemp,
    CSV_GetSWVersion,
    CSV_SetDateTime,
    EDM_GetEglIntensity,
    EDM_Laserpointer,
    EDM_SetEglIntensity,
    SUP_GetConfig,
    SUP_SetConfig,
    TMC_DoMeasure,
    TMC_GetAngle1,
    TMC_GetAngle5,
    TMC_GetAngSwitch,
    TMC_GetAtmCorr,
    TMC_GetCoordinate,
    TMC_GetEdmMode,
    TMC_GetFace,
    TMC_GetHeight,
    TMC_GetInclineSwitch,
    TMC_GetPrismCorr,
    TMC_GetRefractiveCorr,
    TMC_GetRefractiveMethod,
    TMC_GetSignal,
    TMC_GetSimpleCoord,
    TMC_GetSimpleMea,
    TMC_GetSlopeDistCorr,
    TMC_GetStation,
    TMC_IfDataAzeCorrError,
    TMC_IfDataIncCorrError,
    TMC_QuickDist,
    TMC_SetAngSwitch,
    TMC_SetAtmCorr,
    TMC_SetEdmMode,
    TMC_SetHandDist,
    TMC_SetHeight,
    TMC_SetInclineSwitch,
    TMC_SetOrientation,
    TMC_SetRefractiveCorr,
    TMC_SetRefractiveMethod,
    TMC_SetStation]
    
if __name__=="__main__":
    set_station = TMC_SetStation()
    print(f"Code for set station: {set_station.gc_command}")

