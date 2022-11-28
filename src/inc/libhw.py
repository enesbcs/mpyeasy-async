try:
 from machine import Pin, I2C, SPI, UART, freq, reset, unique_id
except:
 from inc.machine import Pin, I2C, SPI, UART, freq, reset, unique_id
import settings
import gc

def gethwtype():
  hw = 0 #fake
  try:
   from esp32 import Partition
   hw = 1 #esp32
  except:
   hw=0
  if hw==0:
   try:
    from rp2 import PIOASMError
    hw = 2 #rp2
   except:
    hw=0
  return hw

i2c0 = None
i2c1 = None
spi1 = None
spi2 = None
uart1 = None
uart2 = None

I2CDevices = [
 {"name": "MCP9808 Temp sensor",
  "addr": [0x18,0x19,0x1A,0x1B,0x1C,0x1D,0x1E,0x1F]},
 {"name": "Chirp! Water sensor",
  "addr": [0x20]},
 {"name": "MCP23008/MCP23017 I2C GPIO expander; LCD1602; PCF8574",
  "addr": [0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27]},
 {"name": "PCF8574A",
  "addr": [0x38,0x39,0x3A,0x3B,0x3C,0x3D,0x3E,0x3F]},
 {"name": "PN532",
  "addr": [0x24]},
 {"name": "VL53L0x",
  "addr": [0x29]},
 {"name": "VL6180X ToF sensor",
  "addr": [0x29]},
 {"name": "TSL2561 light sensor",
  "addr": [0x29,0x39,0x49]},
 {"name": "AXP192",
  "addr": [0x34]},
 {"name": "APDS-9960 IR/Color/Proximity Sensor",
  "addr": [0x39]},
 {"name": "SSD1305/SSD1306 monochrome OLED",
  "addr": [0x3C,0x3D]},
 {"name": "HTU21D-F/Si7021 Humidity/Temp sensor",
  "addr": [0x40]},
 {"name": "INA219 Current sensor",
  "addr": [0x40,0x41,0x44,0x45]},
 {"name": "PCA9685 PWM extender",
  "addr": [0x40,0x41,0x42,0x43,0x44,0x45,0x46,0x47,0x48,0x49,0x4A,0x4B,0x4C,0x4D,0x4E,0x4F,0x50,0x51,0x52,0x53,0x54,0x55,0x56,0x57,0x58,0x59,0x5A,0x5B,0x5C,0x5D,0x5E,0x5F,0x60,0x61,0x62,0x63,0x64,0x65,0x66,0x67,0x68,0x69,0x6A,0x6B,0x6C,0x6D,0x6E,0x6F,0x71,0x72,0x73,0x74,0x75,0x76,0x77]},
 {"name": "SHT30/31/35 Humidity/Temp sensor",
  "addr": [0x44,0x45]},
 {"name": "PN532 NFC/RFID reader",
  "addr": [0x48]},
 {"name": "ADS1115/ADS1015 4-channel ADC",
  "addr": [0x48,0x49,0x4A,0x4B]},
 {"name": "LM75A; PCF8591; MCP3221",
  "addr": [0x48,0x49,0x4A,0x4B,0x4C,0x4D,0x4E,0x4F]},
 {"name": "MAX44009 ambient light sensor",
  "addr": [0x4A]},
 {"name": "BH1750",
  "addr": [0x23,0x5C]},
 {"name": "BM8563",
  "addr": [0x51]},
 {"name": "MPR121 touch sensor",
  "addr": [0x5a,0x5b,0x5c,0x5d]},
 {"name": "DHT12/AM2320",
  "addr": [0x5C]},
 {"name": "MCP4725 DAC",
  "addr": [0x60,0x61]},
 {"name": "DS1307/DS3231/PCF8523 RTC;MPU6886",
  "addr": [0x68]},
 {"name": "MPU6050 Triple axis gyroscope & accelerometer",
  "addr": [0x68,0x69]},
 {"name": "PCA9685 'All Call'",
  "addr": [0x70]},
 {"name": "BMP085/BMP180 Temp/Barometric",
  "addr": [0x77]},
 {"name": "HT16K33",
  "addr": [0x70,0x71,0x72,0x73,0x74,0x75,0x76,0x77]},
 {"name": "BMP280 Temp/Barometric;BME180 Temp/Barometric/Humidity",
  "addr": [0x76,0x77]},
 {"name": "ProMini Extender (standard)",
  "addr": [0x3F,0x4F,0x5F,0x6F]},
 {"name": "ProMini Extender (non-standard)",
  "addr": [0x7F]}

]

def geti2cdevname(devaddr):
 global I2CDevices
 name = ""
 for i in range(len(I2CDevices)):
  if int(devaddr) in I2CDevices[i]["addr"]:
   if name!="":
    name += "; "
   name += I2CDevices[i]["name"]
 if name == "":
  name = "Unknown"
 return name

def initi2c(num,iscl,isda,ifreq=100000,force=False):
 global i2c0, i2c1
 if num==0:
  if i2c0 is None or force:
   i2c0 = I2C(num,scl=Pin(iscl),sda=Pin(isda),freq=ifreq)
  return i2c0
 else:
  if i2c1 is None or force:
   i2c1 = I2C(num,scl=Pin(iscl),sda=Pin(isda),freq=ifreq)
  return i2c1
 return None

def initspi2(num,isck,imosi,imiso,baudrate=10000000):
 global spi1, spi2
 if num == 1:
   if spi1 is None:
    spi1 = SPI(num,baudrate,sck=Pin(isck), mosi=Pin(imosi), miso=Pin(imiso))
    return spi1
 elif num == 2:
   if spi2 is None:
    spi2 = SPI(num,baudrate,sck=Pin(isck), mosi=Pin(imosi), miso=Pin(imiso))
    return spi2
 return None

def inituart(num,utx,urx,utimeout=10000,ubaud=9600):
 global uart1, uart2
 if num == 1:
   if uart1 is None:
    uart1 = UART(num,tx=utx,rx=urx,baudrate=ubaud,timeout=utimeout)
    return uart1
 elif num == 2:
   if uart2 is None:
    uart2 = UART(num,tx=utx,rx=urx,baudrate=ubaud,timeout=utimeout)
    return uart2
 return None

def initgpio():
 pins = []
 for p in settings.Pinout:
    pnum = p
    try:
     pnum = p['p']
     if p['m'] == 1: #input
      pins.append(Pin(pnum, Pin.IN))
     elif p['m'] == 2: #input pulldown
      pins.append(Pin(pnum, Pin.IN, Pin.PULL_DOWN))
     elif p['m'] == 3: #input pullup
      pins.append(Pin(pnum, Pin.IN, Pin.PULL_UP))
     elif p['m'] == 4: #output
      pins.append(Pin(pnum, Pin.OUT))
     elif p['m'] == 5: #output lo
      pins.append(Pin(pnum, Pin.OUT, value=0))
     elif p['m'] == 6: #output hi
      pins.append(Pin(pnum, Pin.OUT, value=1))
    except Exception as e:
     print("Init D",pnum,str(e))

def setgpio(pnum):
 pino = None
 try:
  for p in settings.Pinout:
   try:
    if pnum == p['p']:
     if p['m'] == 1: #input
      pino = Pin(pnum, Pin.IN)
     elif p['m'] == 2: #input pulldown
      pino = Pin(pnum, Pin.IN, Pin.PULL_DOWN)
     elif p['m'] == 3: #input pullup
      pino = Pin(pnum, Pin.IN, Pin.PULL_UP)
     elif p['m'] == 4: #output
      pino = Pin(pnum, Pin.OUT)
     elif p['m'] == 5: #output lo
      pino = Pin(pnum, Pin.OUT, value=0)
     elif p['m'] == 6: #output hi
      pino = Pin(pnum, Pin.OUT, value=1)
   except Exception as e:
     print("Set D",pnum,str(e))
 except:
  pass
 return pino

def geti2clist():
 il = []
 if i2c0 is not None:
  il.append(0)
 if i2c1 is not None:
  il.append(1)
 return il

def getspilist():
 il = []
 if spi1 is not None:
  il.append(1)
 if spi2 is not None:
  il.append(2)
 return il

def inithw():
 try:
  if settings.HW['freq']>0:
   setfreq(settings.HW['freq'])
 except:
  pass
 #init gpio,i2c,spi
 try:
   settings.loadpinout()
   initgpio() #restore pin states
 except Exception as e:
   print("Error loading pinout settings")
 try:
   if settings.HW['i2c0']:
    initi2c(0,settings.HW['i2c0-scl'],settings.HW['i2c0-sda'],settings.HW['i2c0-freq'])
 except Exception as e:
   print("hwi",e)
 try:
   if settings.HW['i2c1']:
    initi2c(1,settings.HW['i2c1-scl'],settings.HW['i2c1-sda'],settings.HW['i2c1-freq'])
 except Exception as e:
   print("hwi",e)
 cspi = False
 try:
   if settings.HW['spic']: #spi1???
    libhw.initspi2(1,settings.HW['spic-clk'],settings.HW['spic-mosi'],settings.HW['spic-miso'],settings.HW['spic-baud'])
    cspi = True
 except Exception as e:
   print("hwic",e)

def getfreq():
 try:
  f = freq()
 except:
  f = 0
 return f

def setfreq(freq):
 try:
  freq(freq)
 except:
  pass

def get_memory():
  ret = {'f':0,'u':0,'t':0}
  f = False
  try:
   gc.collect()
   ret['f'] = gc.mem_free()
   ret['u'] = gc.mem_alloc()
   ret['t'] = ret['u'] + ret['f']
  except:
   f = True
  if f: # try other ways
   try:
    import resource
    ret['u']= resource.getrusage(resource.RUSAGE_SELF)[2] * 1024
   except:
    pass
   try:
    import os
    ret['t'] = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    ret['f']  = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_AVPHYS_PAGES')
   except:
    pass
  return ret

def FreeMem():
  try:
   gc.collect()
   ret = gc.mem_free()
  except:
   ret = -1
  if ret==-1:
   ret = get_memory()['f']
  return ret

def reboot():
  try:
   reset()
  except:
   pass

def getid():
  try:
   return unique_id()
  except:
   return False
