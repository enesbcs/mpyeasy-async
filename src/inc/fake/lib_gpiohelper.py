import pglobals
import settings
import inc.misc as misc
import inc.utime as utime

commandlist = ["gpio","pulse"]

hiddenpins = 0
MAX_GPIO=17

def is_pin_analog(pin):
    return False

def is_pin_touch(pin):
    return False

def is_pin_valid(pin):
    if int(pin)<17:
     return True
    else:
     return False

def is_pin_dac(pin):
    return False

def is_pin_pwm(pin):
    res = (int(pin) in [15,16])
    return res

def syncvalue(bcmpin,value):
 from commands import rulesProcessing
 for x in range(0,len(settings.Tasks)):
  if (settings.Tasks[x]) and type(settings.Tasks[x]) is not bool: # device exists
   if (settings.Tasks[x].enabled):
     if (settings.Tasks[x].pluginid==29) and (settings.Tasks[x].taskdevicepin[0]==bcmpin): # output on specific pin
      settings.Tasks[x].uservar[0] = value
      if settings.Tasks[x].valuenames[0]!= "":
       rulesProcessing(settings.Tasks[x].taskname+"#"+settings.Tasks[x].valuenames[0]+"="+str(value),pglobals.RULE_USER)
      settings.Tasks[x].plugin_senddata()
      break

def gpio_commands(cmd):
  from inc.fake.fakemachine import Pin
  res = False
  cmdarr = cmd.split(",")
  cmdarr[0] = cmdarr[0].strip().lower()
  if cmdarr[0] == "gpio":
   pin = -1
   val = -1
   logline = ""
   try:
    pin = int(cmdarr[1].strip())
    val = int(cmdarr[2].strip())
   except:
    pin = -1
   if pin>-1 and val in [0,1]:
    logline = "BCM"+str(pin)+" set to "+str(val)
    misc.addLog(pglobals.LOG_LEVEL_DEBUG,logline)
    suc = False
    try:
     suc = True
     selfpin = Pin(pin,Pin.OUT)
     selfpin.value(val)
     syncvalue(pin,val)
    except Exception as e:
     misc.addLog(pglobals.LOG_LEVEL_ERROR,"BCM"+str(pin)+": "+str(e))
     suc = False
   res = True
  elif cmdarr[0]=="pulse":
   pin = -1
   val = -1
   logline = ""
   try:
    pin = int(cmdarr[1].strip())
    val = int(cmdarr[2].strip())
   except:
    pin = -1
   dur = 100
   try:
    dur = int(cmdarr[3].strip())
   except:
    dur = 100
   if pin>-1 and val in [0,1]:
    logline = "BCM"+str(pin)+": Pulse started"
    misc.addLog(pglobals.LOG_LEVEL_DEBUG,logline)
    try:
     selfpin = Pin(pin,Pin.OUT)
     selfpin.value(val)
     utime.sleep_ms(dur)
     selfpin.value(1-val)
    except Exception as e:
     misc.addLog(pglobals.LOG_LEVEL_ERROR,"BCM"+str(pin)+": "+str(e))
     suc = False
    misc.addLog(pglobals.LOG_LEVEL_DEBUG,"BCM"+str(pin)+": Pulse ended")
   res = True

  return res

def play_tone(pin,rfreq,delay):
  return None

def setservoangle(servopin,angle):
    pass

def play_rtttl(pin,notestr):
 pass
