#############################################################################
################ Rotary encoder plugin for mPyEasy-async ####################
#############################################################################
#
# Copyright (C) 2022 by Alexander Nagy - https://bitekmindenhol.blog.hu/
#
import plugin
import pglobals
import inc.misc as misc
import webserver_global as ws
import inc.utime as utime
try:
 from machine import Pin
except:
 pass

class Plugin(plugin.PluginProto):
 PLUGIN_ID = 59
 PLUGIN_NAME = "Input - Rotary Encoder (TESTING)"
 PLUGIN_VALUENAME1 = "Counter"

 def __init__(self,taskindex): # general init
  plugin.PluginProto.__init__(self,taskindex)
  self.dtype = pglobals.DEVICE_TYPE_DUAL
  self.vtype = pglobals.SENSOR_TYPE_DIMMER
  self.valuecount = 1
  self.senddataoption = True
  self.timeroption = False
  self.timeroptional = True
  self.inverselogicoption = False
  self.recdataoption = False
  self.dtlast = -1
  self.clklast = -1
  self.timer100ms = False
  self._pin1 = None
  self._pin2 = None
  self.inprogress = False
  self.lastsend = 0

 def plugin_exit(self):
  self.timer100ms = False
  return True

 def plugin_init(self,enableplugin=None):
  plugin.PluginProto.plugin_init(self,enableplugin)
  self.decimals[0]=1
  self.inprogress = False
  try:
   if float(self.uservar[0])<float(self.taskdevicepluginconfig[1]): # minvalue check
    self.set_value(1,self.taskdevicepluginconfig[1],False)
   if float(self.uservar[0])>float(self.taskdevicepluginconfig[2]): # maxvalue check
    self.set_value(1,self.taskdevicepluginconfig[2],False)
  except:
    self.set_value(1,self.taskdevicepluginconfig[1],False)
  if int(self.taskdevicepin[0])>=0 and self.enabled and int(self.taskdevicepin[1])>=0:
   import inc.libhw as libhw
   try:
    self._pin1 = libhw.setgpio(int(self.taskdevicepin[0]))
    self._pin2 = libhw.setgpio(int(self.taskdevicepin[1]))
   except:
    pass
   try:
    self.clklast = self._pin1.value()
    self.timer100ms = True
    self.initialized = True
   except:
    misc.addLog(pglobals.LOG_LEVEL_ERROR,"Event can not be added")
    self.initialized = False
  else:
   self.initialized = False

 def webform_load(self): # create html page for settings
  ws.addFormNote("1st GPIO=CLK, 2nd GPIO=DT, BOTH of them needs to be INPUT-PULLUP")
  choice1 = float(self.taskdevicepluginconfig[0])
  ws.addFormFloatNumberBox("Step","p059_step",choice1,-100,100)
  try:
   minv = int(self.taskdevicepluginconfig[1])
  except:
   minv = 0
  ws.addFormNumericBox("Limit min.","p059_min",minv,-65535,65535)
  try:
   maxv = int(self.taskdevicepluginconfig[2])
  except:
   maxv = 100
  if minv>=maxv:
   maxv = minv+1
  ws.addFormNumericBox("Limit max.","p059_max",maxv,-65535,65535)
  return True

 def webform_save(self,params): # process settings post reply
  changed = False
  par = ws.arg("p059_step",params)
  if par == "":
    par = 1
  if str(self.taskdevicepluginconfig[0]) != str(par):
   changed = True
  try:
   self.taskdevicepluginconfig[0] = float(par)
  except:
   self.taskdevicepluginconfig[0] = 1
  par = ws.arg("p059_min",params)
  if par == "":
    par = 0
  if str(self.taskdevicepluginconfig[1]) != str(par):
   changed = True
  try:
   self.taskdevicepluginconfig[1] = float(par)
  except:
   self.taskdevicepluginconfig[1] = 0
  par = ws.arg("p059_max",params)
  if par == "":
    par = 100
  if float(self.taskdevicepluginconfig[1])>=float(par):
    par = float(self.taskdevicepluginconfig[1])+1
  if str(self.taskdevicepluginconfig[2]) != str(par):
   changed = True
  try:
   self.taskdevicepluginconfig[2] = float(par)
  except:
   self.taskdevicepluginconfig[2] = 100

  if changed:
   self.plugin_init()
  return True

 def timer_ten_per_second(self):
  if self.initialized and self.enabled:
    self.p059_handler(0)

 def p059_handler(self,channel):
  if (self.inprogress==False):
   try:
    self.inprogress = True
    aclk = self._pin1.value()
    if aclk != self.clklast:
     self.dtlast = self._pin2.value()
     try:
      ac = float(self.uservar[0])
     except:
      ac = 0
     if self.dtlast !=  aclk:
      if ac<float(self.taskdevicepluginconfig[2]):
       ac += float(self.taskdevicepluginconfig[0])
     else:
      if ac>float(self.taskdevicepluginconfig[1]):
       ac -= float(self.taskdevicepluginconfig[0])
     self.clklast = aclk
     atime = utime.ticks_ms()
     if atime - self.lastsend > 200:
      rep = True
      self.lastsend = atime
     else:
      rep = False
     self.set_value(1,ac,rep)
     self._lastdataservetime = atime
    self.inprogress = False
   except Exception as e:
    self.inprogress = False
