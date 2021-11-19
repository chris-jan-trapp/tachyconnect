from . import gc_constants as gc
from .ts_control import GeoCOMCommand, GSICommand, CommunicationConstants


class TachyRequest:
    gsi_command = ""
    gc_command = ""
    unpacking_keys = {}

    def __init__(self, time_out = 2, *args) -> None:
        self.gc_command = str(gc.COMMAND_CODES.get(self.label))
        self.time_out = time_out
        self.args = args

    @property
    def label(self):
        return self.__class__.__name__

    def __str__(self) -> str:
        return f"{self.label}: {', '.join(self.args) if len(self.args) else 'No args'}, {self.time_out} seconds"

    def get_gsi_command(self):
        if self.gsi_command == "":
            raise NotImplementedError(f'No GSI command for {self.label}')
        return GSICommand(self.gsi_command, self.label, self.time_out, *self.args)
    
    def get_geocom_command(self):
        return GeoCOMCommand(self.gc_command, self.label, self.time_out, *self.args)


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
    pass


class COM_SwitchOnTPS(TachyRequest):
    pass


class CSV_GetDateTime(TachyRequest):
    pass


class CSV_GetDeviceConfig(TachyRequest):
    pass


class CSV_GetInstrumentName(TachyRequest):
    pass


class CSV_GetInstrumentNo(TachyRequest):
    pass


class CSV_GetIntTemp(TachyRequest):
    pass


class CSV_GetSWVersion(TachyRequest):
    pass


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
    pass


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


if __name__=="__main__":
    set_station = TMC_SetStation()
    print(f"Code for set station: {set_station.gc_command}")