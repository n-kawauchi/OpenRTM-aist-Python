#!/usr/bin/env python
# -*- Python -*-

import sys

import OpenRTM_aist
import RTC

consolein_spec = ["implementation_id", "ConsoleIn",
                  "type_name",         "ConsoleIn",
                  "description",       "Console input component",
                  "version",           "1.0",
                  "vendor",            "Shinji Kurihara",
                  "category",          "example",
                  "activity_type",     "DataFlowComponent",
                  "max_instance",      "10",
                  "language",          "Python",
                  "lang_type",         "script",
                  ""]


class ConsoleIn(OpenRTM_aist.DataFlowComponentBase):
  def __init__(self, manager):
    OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
    return
        
  def onInitialize(self):
    self._data = RTC.TimedLong(RTC.Time(0,0),0)
    self._outport = OpenRTM_aist.OutPort("out", self._data)
    # Set OutPort buffer
    self.addOutPort("out", self._outport)
    return RTC.RTC_OK

  def onExecute(self, ec_id):
    print "Please input number: ",
    self._data.data = long(sys.stdin.readline())
    print "Sending to subscriber: ", self._data.data
    self._outport.write()
    return RTC.RTC_OK


def MyModuleInit(manager):
  profile = OpenRTM_aist.Properties(defaults_str=consolein_spec)
  manager.registerFactory(profile,
                          ConsoleIn,
                          OpenRTM_aist.Delete)

  # Create a component
  comp = manager.createComponent("ConsoleIn")
  return


def main():
  # Initialize manager
  mgr = OpenRTM_aist.Manager.init(sys.argv)
  
  # Set module initialization proceduer
  # This procedure will be invoked in activateManager() function.
  mgr.setModuleInitProc(MyModuleInit)

  # Activate manager and register to naming service
  mgr.activateManager()
  
  # run the manager in blocking mode
  # runManager(False) is the default
  mgr.runManager()
  
  # If you want to run the manager in non-blocking mode, do like this
  # mgr.runManager(True)

if __name__ == "__main__":
  main()
