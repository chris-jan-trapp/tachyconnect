from ts_control import CommunicationConstants, GeoCOMCommand, GSICommand

class TachyRequest:
    label = ""
    gc_command = None
    gsi_command = None
    gsi_keys = []

    def create(self, dialect, time_out = 2, *args):
        if dialect == CommunicationConstants.GEOCOM and self.gc_command:
            return GeoCOMCommand(self.gc_command, *args, time_out=time_out)
        if dialect == CommunicationConstants.GSI and self.gsi_command:
            return GSICommand(self.gc_command, *args, time_out=time_out)
        raise NotImplementedError(f"{self.label} is not implemented for {dialect}.")
        
    
class TsFunctionProvider:
    def __init__(self, dialects: DialectLog) -> None:
        self.dialects = dialects

    def abstract_function(self, geoCOM_command, gsi_command,*args)

    def do_beepalarm(self, *args):
        pass
        
    def do_beepnormal(self, *args):
        pass
        
    def do_ifdataazecorrerror(self, *args):
        pass
        
    def do_ifdatainccorrerror(self, *args):
        pass
        
    def do_laserpointer(self, *args):
        pass
        
    def do_measure(self, *args):
        pass
        
    def do_nullproc(self, *args):
        pass
        
    def do_quickdist(self, *args):
        pass
        
    def do_switchofftps(self, *args):
        pass
        
    def do_switchontps(self, *args):
        pass
        
    def get_angle1(self, *args):
        pass
        
    def get_angle5(self, *args):
        pass
        
    def get_angswitch(self, *args):
        pass
        
    def get_atmcorr(self, *args):
        pass
        
    def get_config(self, *args):
        pass
        
    def get_coordinate(self, *args):
        pass
        
    def get_datetime(self, *args):
        pass
        
    def get_deviceconfig(self, *args):
        pass
        
    def get_doubleprecision(self, *args):
        pass
        
    def get_edmmode(self, *args):
        pass
        
    def get_eglintensity(self, *args):
        pass
        
    def get_face(self, *args):
        pass
        
    def get_height(self, *args):
        pass
        
    def get_inclineswitch(self, *args):
        pass
        
    def get_instrumentname(self, *args):
        pass
        
    def get_instrumentno(self, *args):
        pass
        
    def get_inttemp(self, *args):
        pass
        
    def get_prismcorr(self, *args):
        pass
        
    def get_refractivecorr(self, *args):
        pass
        
    def get_refractivemethod(self, *args):
        pass
        
    def get_signal(self, *args):
        pass
        
    def get_simplecoord(self, *args):
        pass
        
    def get_simplemea(self, *args):
        pass
        
    def get_slopedistcorr(self, *args):
        pass
        
    def get_station(self, *args):
        pass
        
    def get_swversion(self, *args):
        pass
        
    def get_swversion(self, *args):
        pass
        
    def set_angswitch(self, *args):
        pass
        
    def set_atmcorr(self, *args):
        pass
        
    def set_config(self, *args):
        pass
        
    def set_datetime(self, *args):
        pass
        
    def set_doubleprecision(self, *args):
        pass
        
    def set_edmmode(self, *args):
        pass
        
    def set_eglintensity(self, *args):
        pass
        
    def set_handdist(self, *args):
        pass
        
    def set_height(self, *args):
        pass
        
    def set_inclineswitch(self, *args):
        pass
        
    def set_orientation(self, *args):
        pass
        
    def set_refractivecorr(self, *args):
        pass
        
    def set_refractivemethod(self, *args):
        pass
        
    def set_station(self, *args):
        pass
        
