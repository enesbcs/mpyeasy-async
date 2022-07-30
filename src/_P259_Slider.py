#############################################################################
#################### GPIO Slider plugin for mPyEasy #########################
#############################################################################
#
# Copyright (C) 2022 by Alexander Nagy - https://bitekmindenhol.blog.hu/
#
import plugin
import pglobals
import inc.misc as misc
import webserver_global as ws
import settings
import inc.utime as utime
try:
 from machine import Pin
except:
 pass

class Plugin(plugin.PluginProto):
 PLUGIN_ID = 259
 PLUGIN_NAME = "Input - Slider (TESTING)"
 PLUGIN_VALUENAME1 = "Dimmer"

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
  self.timer100ms = False
  self._pin1 = None
  self._pin2 = None
  self.inprogress = False

 def plugin_exit(self):
  if self.enabled and self.timer100ms==False:
   try:
    self._pin1.irq(handler=None)
   except:
    pass
   try:
    self._pin2.irq(handler=None)
   except:
    pass
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
    self._pin1.irq(handler=None)
    self._pin2 = libhw.setgpio(int(self.taskdevicepin[1]))
    self._pin2.irq(handler=None)
   except:
    pass
   trig1 = None
   trig2 = None
   for p in settings.Pinout:
     if p['p']== int(self.taskdevicepin[0]):
       if p['m'] == 2: #ipdn
        trig1 = Pin.IRQ_RISING
       elif p['m'] == 3: #ipup
        trig1 = Pin.IRQ_FALLING
     elif p['p']== int(self.taskdevicepin[1]):
       if p['m'] == 2: #ipdn
        trig2 = Pin.IRQ_RISING
       elif p['m'] == 3: #ipup
        trig2 = Pin.IRQ_FALLING
   try:
    self._pin1.irq(trigger=trig1,handler=self.p259_handler)
    self._pin2.irq(trigger=trig2,handler=self.p259_handler)
    self.initialized = True
   except:
    misc.addLog(pglobals.LOG_LEVEL_ERROR,"Event can not be added")
    self.initialized = False
  else:
   self.initialized = False

 def webform_load(self): # create html page for settings
  ws.addFormNote("First button decrease, second increase dim value. Use INPUT-PULLUP or INPUT-PULLDOWN types!")
  choice1 = float(self.taskdevicepluginconfig[0])
  ws.addFormFloatNumberBox("Step","p259_step",choice1,-100,100)
  try:
   minv = int(self.taskdevicepluginconfig[1])
  except:
   minv = 0
  ws.addFormNumericBox("Limit min.","p259_min",minv,-65535,65535)
  try:
   maxv = int(self.taskdevicepluginconfig[2])
  except:
   maxv = 100
  if minv>=maxv:
   maxv = minv+1
  ws.addFormNumericBox("Limit max.","p259_max",maxv,-65535,65535)
  return True

 def webform_save(self,params): # process settings post reply
  changed = False
  par = ws.arg("p259_step",params)
  if par == "":
    par = 1
  if str(self.taskdevicepluginconfig[0]) != str(par):
   changed = True
  try:
   self.taskdevicepluginconfig[0] = float(par)
  except:
   self.taskdevicepluginconfig[0] = 1
  par = ws.arg("p259_min",params)
  if par == "":
    par = 0
  if str(self.taskdevicepluginconfig[1]) != str(par):
   changed = True
  try:
   self.taskdevicepluginconfig[1] = float(par)
  except:
   self.taskdevicepluginconfig[1] = 0
  par = ws.arg("p259_max",params)
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

 def p259_handler(self,channel):
  if self.initialized and self.enabled and (self.inprogress==False):
   try:
    self.inprogress = True
    try:
      ac = float(self.uservar[0])
    except:
      ac = 0
    print(ac)
    if int(channel) == int(self.taskdevicepin[0]): #down
      if ac>float(self.taskdevicepluginconfig[1]):
       ac -= float(self.taskdevicepluginconfig[0])
    else:
      if ac<float(self.taskdevicepluginconfig[2]):
       ac += float(self.taskdevicepluginconfig[0])
    print(ac,float(self.taskdevicepluginconfig[0]))
    self.set_value(1,ac,True)
    self._lastdataservetime = utime.ticks_ms()
    self.inprogress = False
   except Exception as e:
    print(e)
    self.inprogress = False
