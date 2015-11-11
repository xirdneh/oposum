import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time
from server import *

class OposmSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "oposumSrvc"
    _svc_display_name_ = "oposum Service"
    stop_event = win32event.CreateEvent(None,0,0,None)
    
    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        socket.setdefaulttimeout(60)
        self.stop_requested = False

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.stop_requested = True

    def SvcDoRun(self):

        import servicemanager      
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,servicemanager.PYS_SERVICE_STARTED,(self._svc_name_, '')) 
      
        #self.timeout = 640000    #640 seconds / 10 minutes (value is in milliseconds)
        self.timeout = 1000     #120 seconds / 2 minutes
        # This is how long the service will wait to run / refresh itself (see script below)
        self.server = SimpleHttpServer('0.0.0.0', 9099)
        self.server.start()
        #server.waitForThread()
        while 1:
            # Wait for service stop signal, if I timeout, loop again
            rc = win32event.WaitForSingleObject(self.stop_event, self.timeout)
            # Check to see if self.hWaitStop happened
            if rc == win32event.WAIT_OBJECT_0:
                # Stop signal encountered
                self.server.stop()
                servicemanager.LogInfoMsg("SomeShortNameVersion - STOPPED!")  #For Event Log
                break
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STOPPED,
                              (self._svc_name_, ''))
        return

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(OposmSvc)
