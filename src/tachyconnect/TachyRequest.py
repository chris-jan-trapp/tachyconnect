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


class COM_NullProc(TachyRequest):
    pass
    
    
class COM_Local(TachyRequest):
    pass
    
    
class COM_SetDoublePrecision(TachyRequest):
    pass
    
    
class COM_GetDoublePrecision(TachyRequest):
    pass
    
    
class COM_SetSendDelay(TachyRequest):
    pass


class COM_GetBinaryAvailable(TachyRequest):
    pass
    
    
class COM_SetBinaryAvailable(TachyRequest):
    pass
    
    
class COM_GetSWVersion(TachyRequest):
    gsi_command = "GET/I/WI593;"
    
    
class COM_SwitchOnTPS(TachyRequest):
    gsi_command = "a"
    
    
class COM_SwitchOffTPS(TachyRequest):
    gsi_command = "b"
    
    
class COM_EnableSignOff(TachyRequest):
    pass
    
    
class EDM_Laserpointer(TachyRequest):
    pass
    
    
class EDM_SetBumerang(TachyRequest):
    pass
    
    
class EDM_On(TachyRequest):
    pass
    
    
class EDM_SetTrkLightSwitch(TachyRequest):
    pass
    
    
class EDM_SetTrkLightBrightness(TachyRequest):
    pass
    
    
class EDM_GetTrkLightSwitch(TachyRequest):
    pass
    
    
class EDM_GetTrkLightBrightness(TachyRequest):
    pass
    
    
class EDM_GetBumerang(TachyRequest):
    pass
    
    
class EDM_GetEglIntensity(TachyRequest):
    pass
    
    
class EDM_SetEglIntensity(TachyRequest):
    pass
    
    
class TMC_GetAngle1(TachyRequest):
    pass
    
    
class TMC_SetInclineSwitch(TachyRequest):
    pass
    
    
class TMC_GetInclineSwitch(TachyRequest):
    pass
    
    
class TMC_DoMeasure(TachyRequest):
    pass
    
    
class TMC_GetStation(TachyRequest):
    pass
    
    
class TMC_SetStation(TachyRequest):
    pass
     
    
class TMC_GetHeight(TachyRequest):
    gsi_command = "GET/I/WI88"
    
    
class TMC_SetHeight(TachyRequest):
    pass
    
    
class TMC_GetAngSwitch(TachyRequest):
    pass
    
    
class TMC_SetAngSwitch(TachyRequest):
    pass
    
    
class TMC_SetHandDist(TachyRequest):
    pass
    
    
class TMC_SetEdmMode(TachyRequest):
    pass
    
    
class TMC_GetEdmMode(TachyRequest):
    pass
    
    
class TMC_GetSignal(TachyRequest):
    pass
    
    
class TMC_GetPrismCorr(TachyRequest):
    pass
    
    
class TMC_SetPrismCorr(TachyRequest):
    pass
    
    
class TMC_GetFace(TachyRequest):
    pass
    
    
class TMC_SetAtmCorr(TachyRequest):
    pass
    
    
class TMC_GetAtmCorr(TachyRequest):
    pass
    
    
class TMC_SetRefractiveCorr(TachyRequest):
    pass
   
    
class TMC_GetRefractiveCorr(TachyRequest):
    gsi_command = "GET/I/WI538"
    
    
class TMC_GetCoordinate(TachyRequest):
    pass
    
    
class TMC_GetCoordinate1(TachyRequest):
    pass
    
    
class TMC_SetRefractiveMethod(TachyRequest):
    pass
    
    
class TMC_GetRefractiveMethod(TachyRequest):
    pass
    
    
class TMC_GetAngle5(TachyRequest):
    pass
    
    
class TMC_GetSimpleMea(TachyRequest):
    pass
    
    
class TMC_SetOrientation(TachyRequest):
    pass
    
    
class TMC_IfDataAzeCorrError(TachyRequest):
    pass
    
    
class TMC_IfDataIncCorrError(TachyRequest):
    pass
    
    
class TMC_GetSimpleCoord(TachyRequest):
    pass
    
    
class TMC_QuickDist(TachyRequest):
    pass
    
    
class TMC_GetSlopeDistCorr(TachyRequest):
    pass
    
    
class CSV_GetInstrumentNo(TachyRequest):
    pass
      
    
class CSV_GetInstrumentName(TachyRequest):
    gsi_command = "GET/I/WI13"
    
    
class CSV_SetUserInstrumentName(TachyRequest):
    pass
    
    
class CSV_GetUserInstrumentName(TachyRequest):
    pass
    
    
class CSV_SetDateTime(TachyRequest):
    pass
    
    
class CSV_GetDateTime(TachyRequest):
    pass
    
    
class CSV_GetVBat(TachyRequest):
    pass
    
    
class CSV_GetVMem(TachyRequest):
    pass
    
    
class CSV_GetIntTemp(TachyRequest):
    pass
    
    
class CSV_GetSWVersion(TachyRequest):
    pass
    
    
class CSV_GetSWVersion2(TachyRequest):
    pass
    
    
class CSV_GetDeviceConfig(TachyRequest):
    pass
    
    
class MOT_StartController(TachyRequest):
    pass
    
    
class MOT_StopController(TachyRequest):
    pass
    
    
class MOT_SetVelocity(TachyRequest):
    pass
    
    
class MOT_ReadLockStatus(TachyRequest):
    pass
    
    
class WIR_GetRecFormat(TachyRequest):
    pass
    
    
class WIR_SetRecFormat(TachyRequest):
    pass
    
    
class AUT_SetTol(TachyRequest):
    pass
    
    
class AUT_ReadTol(TachyRequest):
    pass
    
    
class AUT_SetTimeout(TachyRequest):
    pass
    
    
class AUT_ReadTimeout(TachyRequest):
    pass
    
    
class AUT_LockIn(TachyRequest):
    pass
    
    
class AUT_SetATRStatus(TachyRequest):
    pass
    
    
class AUT_GetATRStatus(TachyRequest):
    pass
    
    
class AUT_SetLockStatus(TachyRequest):
    pass
    
    
class AUT_GetLockStatus(TachyRequest):
    pass
    
    
class AUT_MakePositioning(TachyRequest):
    pass
    
    
class AUT_MakePositioning4(TachyRequest):
    pass
    
    
class AUT_ChangeFace(TachyRequest):
    pass
    
    
class AUT_ChangeFace4(TachyRequest):
    pass
    
    
class AUT_Search(TachyRequest):
    pass
    
    
class AUT_Search2(TachyRequest):
    pass
    
    
class AUT_GetFineAdjustMode(TachyRequest):
    pass
    
    
class AUT_SetFineAdjustMode(TachyRequest):
    pass
    
    
class AUT_FineAdjust(TachyRequest):
    pass
    
    
class AUT_FineAdjust3(TachyRequest):
    pass
    
    
class AUT_GetUserSpiral(TachyRequest):
    pass
    
    
class AUT_SetUserSpiral(TachyRequest):
    pass
    
    
class AUT_GetSearchArea(TachyRequest):
    pass
    
    
class AUT_SetSearchArea(TachyRequest):
    pass
    
    
class AUT_PS_SetRange(TachyRequest):
    pass
    
    
class AUT_PS_EnableRange(TachyRequest):
    pass
    
    
class AUT_PS_SearchNext(TachyRequest):
    pass
    
    
class AUT_PS_SearchWindow(TachyRequest):
    pass
    
    
class BMM_BeepOn(TachyRequest):
    pass
    
    
class BMM_BeepOff(TachyRequest):
    pass
    
    
class BMM_BeepNormal(TachyRequest):
    pass
    
    
class BMM_BeepAlarm(TachyRequest):
    pass
    
    
class CTL_GetUpCounter(TachyRequest):
    pass
    
    
class SUP_GetConfig(TachyRequest):
    pass
    
    
class SUP_SetConfig(TachyRequest):
    pass
    
    
class SUP_SwitchLowTempControl(TachyRequest):
    pass
    
    
class BAP_GetLastDisplayedError(TachyRequest):
    pass
    
    
class BAP_SetPrismType(TachyRequest):
    pass
    
    
class BAP_GetPrismType(TachyRequest):
    pass
    
    
class BAP_MeasDistanceAngle(TachyRequest):
    pass
    
    
class BAP_GetMeasPrg(TachyRequest):
    pass
    
    
class BAP_SetMeasPrg(TachyRequest):
    pass
    
    
class BAP_SearchTarget(TachyRequest):
    pass
    
    
class BAP_SetTargetType(TachyRequest):
    pass
    
    
class BAP_GetTargetType(TachyRequest):
    pass
    
    
class BAP_GetPrismDef(TachyRequest):
    pass
    
    
class BAP_SetPrismDef(TachyRequest):
    pass
    
    
class AUS_SetUserAtrState(TachyRequest):
    pass
    
    
class AUS_GetUserAtrState(TachyRequest):
    pass
    
    
class AUS_SetUserLockState(TachyRequest):
    pass
    
    
class AUS_GetUserLockState(TachyRequest):
    pass
    
    
class AUS_SwitchRcsSearch(TachyRequest):
    pass
    
    
class AUS_GetRcsSearchSwitch(TachyRequest):
    pass
    
    
class IOS_BeepOff(TachyRequest):
    pass
    
    
class IOS_BeepOn(TachyRequest):
    pass
    
    

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

