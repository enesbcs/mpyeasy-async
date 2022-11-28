#############################################################################
############################# AM2320 for mpyEasy ############################
#############################################################################
#
# Copyright (C) 2022 by Alexander Nagy - https://bitekmindenhol.blog.hu/
#
import plugin
import pglobals
import misc
import webserver_global as ws
import utime
import inc.libhw as libhw
import ustruct

class Plugin(plugin.PluginProto):
 PLUGIN_ID = 51
 PLUGIN_NAME = "Environment - AM2320"
 PLUGIN_VALUENAME1 = "Temperature"
 PLUGIN_VALUENAME2 = "Humidity"

 def __init__(self,taskindex): # general init
  plugin.PluginProto.__init__(self,taskindex)
  self.dtype = pglobals.DEVICE_TYPE_I2C
  self.vtype = pglobals.SENSOR_TYPE_TEMP_HUM
  self.readinprogress = 0
  self.valuecount = 2
  self.senddataoption = True
  self.timeroption = True
  self.timeroptional = False
  self.formulaoption = True
  self._nextdataservetime = 0
  self._temp = None

 def plugin_init(self,enableplugin=None):
  plugin.PluginProto.plugin_init(self,enableplugin)
  self.uservar[0] = 0
  self.uservar[1] = 0
  self.readinprogress = 0
  if self.enabled:
    i2cl = None
    try:
     if int(self.i2c)==0:
      i2cl = libhw.i2c0
     elif int(self.i2c)==1:
      i2cl = libhw.i2c1
    except:
     pass
    try:
     self._temp = AM2320(i2cl)
    except Exception as e:
     self.initialized = False
    if self._temp is None:
     self.initialized = False
    if self.initialized:
     misc.addLog(pglobals.LOG_LEVEL_INFO,"AM2320 initialized")
    else:
     misc.addLog(pglobals.LOG_LEVEL_ERROR,"AM2320 can not be initialized!")

 def plugin_read(self): # deal with data processing at specified time interval
  result = False
  if self.initialized and self.readinprogress==0 and self.enabled:
   self.readinprogress = 1
   try:
    self._temp.measure()
    temp = self._temp.temperature()
    hum  = self._temp.humidity()
    if temp is not None and hum is not None:
     self.set_value(1,temp,False)
     self.set_value(2,hum,False)
   except Exception as e:
    misc.addLog(pglobals.LOG_LEVEL_ERROR,"AM2320 read error! "+str(e))
   self.plugin_senddata()
   self._lastdataservetime = utime.ticks_ms()
   result = True
   self.readinprogress = 0
  return result

class AM2320:
    def __init__(self, i2c=None, address=0x5c):
        self.i2c = i2c
        self.address = address
        self.buf = bytearray(8)
    def measure(self):
        buf = self.buf
        address = self.address
        # wake sensor
        try:
            self.i2c.writeto(address, b'')
        except OSError:
            pass
        # read 4 registers starting at offset 0x00
        self.i2c.writeto(address, b'\x03\x00\x04')
        # wait at least 1.5ms
        utime.sleep_ms(2)
        # read data
        self.i2c.readfrom_mem_into(address, 0, buf)
        crc = ustruct.unpack('<H', bytearray(buf[-2:]))[0]
        if (crc != self.crc16(buf[:-2])):
            raise Exception("checksum error")
    def crc16(self, buf):
        crc = 0xFFFF
        for c in buf:
            crc ^= c
            for i in range(8):
                if crc & 0x01:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc
    def humidity(self):
        return (self.buf[2] << 8 | self.buf[3]) * 0.1
    def temperature(self):
        t = ((self.buf[4] & 0x7f) << 8 | self.buf[5]) * 0.1
        if self.buf[4] & 0x80:
            t = -t
        return t
