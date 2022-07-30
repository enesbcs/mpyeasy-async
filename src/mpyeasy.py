try:
 import uasyncio as asyncio
except ImportError:
 import asyncio
try:
 import utime
 fake = False
except:
 import inc.fake.faketime as utime
 fake = True
import gc
import pglobals
import settings
from commands import rulesProcessing, ExecQueueCmds, splitruletoevents
import inc.misc as misc
import os
from webserver import MicroWebSrv

timer100ms = 0
timer20ms = 0
timer1s = 0
timer2s = 0
timer30s = 0
init_ok = False
prevminute = -1

def timeoutReached(timerval):
   if (utime.ticks_diff(utime.ticks_ms(),timerval)>0):
     return True
   return False

def run50timespersecond():
   for x in range(0,len(settings.Tasks)):
     if (settings.Tasks[x]) and (type(settings.Tasks[x]) is not bool):
      try:
       if (settings.Tasks[x].enabled):
        if (settings.Tasks[x].timer20ms):
         settings.Tasks[x].timer_fifty_per_second()
      except:
       pass

def run10timespersecond():
  for x in range(0,len(settings.Tasks)):
     if (settings.Tasks[x]) and (type(settings.Tasks[x]) is not bool):
      try:
       if (settings.Tasks[x].enabled):
        if (settings.Tasks[x].timer100ms):
         settings.Tasks[x].timer_ten_per_second()
      except:
       pass
  for y in range(0,len(settings.Controllers)):
   if (settings.Controllers[y]):
     try:
      if (settings.Controllers[y].enabled):
       if (settings.Controllers[y].onmsgcallbacksupported): # scheduling needed
        settings.Controllers[y].periodic_check()
     except:
       pass
  try:
   ExecQueueCmds()
  except:
   pass

def runoncepersecond():
   for x in range(0,len(settings.Tasks)):
     if (settings.Tasks[x]) and (type(settings.Tasks[x]) is not bool):
      try:
       if (settings.Tasks[x].enabled):
        if (settings.Tasks[x].timer1s):
         settings.Tasks[x].timer_once_per_second()
      except:
       pass
   checkSensors()

def runon2seconds():
   for x in range(0,len(settings.Tasks)):
     if (settings.Tasks[x]) and (type(settings.Tasks[x]) is not bool):
      try:
       if (settings.Tasks[x].enabled):
        if (settings.Tasks[x].timer2s):
         settings.Tasks[x].timer_two_second()
      except:
       pass

async def runon30seconds():
  for y in range(0,len(settings.Controllers)):
   if (settings.Controllers[y]):
     try:
      if (settings.Controllers[y].enabled):
       if (settings.Controllers[y].timer30s): # scheduling needed
        settings.Controllers[y].timer_thirty_second()
     except:
       pass
  if settings.ISWLAN:
   import inc.unet as unet
   if settings.Settings['WifiAP']==2: #if client notconnected
    if (unet.wifi_sta_isconnected()==False):
      unet.wifi_ap_mode()
   elif settings.Settings['WifiAP']==4: #if lan notconnected
    if (unet.lan_isconnected()==False):
      unet.wifi_ap_mode()
   if (unet.get_active_mode() & 1) == 1: # check wifi connection status
    if unet.wifi_sta_isconnected()==False:
     unet.wifi_sta_disconnect()
     if fake:
          await asyncio.sleep(0.01)
     else:
          await asyncio.sleep_ms(10)
     wificonnect()

def checkSensors():
 for x in range(0,len(settings.Tasks)):
  if (settings.Tasks[x]) and type(settings.Tasks[x]) is not bool: # device exists
   try:
    if (settings.Tasks[x].enabled): # device enabled
     if (settings.Tasks[x].is_read_timely()): # check if device update needed
      settings.Tasks[x].plugin_read()
   except Exception as e:
    pass

def hardwareInit(firstrun=False):
    from inc.libhw import gethwtype, inithw #import inc.libhw as libhw
    if settings.HWType<0:
     settings.HWType = gethwtype()
    if settings.HWType==2 and firstrun:
       settings.Settings["LANIF"] = 1
    print("Init hardware...")
    settings.loadhwsettings()
    inithw()
    try:
     if settings.AdvSettings['dangerouspins']:
      import inc.lib_gpiohelper as gpiohelper
      gpiohelper.hiddenpins=1
    except:
     pass

def setclock():
  ntpres = False
  try:
   if settings.AdvSettings['usentp']:
    import inc.unet as unet
    if (unet.wifi_sta_isconnected() or unet.lan_isconnected()):
     print("NTP time sync")
     ntpres = unet.setntp(settings.AdvSettings['ntpserver'],settings.AdvSettings['timezone'])
     if ntpres:
      misc.start_time = utime.time()
  except:
   pass
  try:
   if settings.AdvSettings['extrtc']>0 and settings.AdvSettings['rtci2c']>=0:
     import inc.mrtc as mrtc
     print("RTC time sync")
     rtcok = False
     try:
      rtca = int(settings.AdvSettings['rtcaddress'])
     except:
      rtca = 0x68
     if settings.AdvSettings['rtci2c']==0:
      rtcok = mrtc.rtcinit(settings.AdvSettings['extrtc'],libhw.i2c0,rtca)
     elif settings.AdvSettings['rtci2c']==1:
      rtcok = mrtc.rtcinit(settings.AdvSettings['extrtc'],libhw.i2c1,rtca)
     if rtcok:
      if ntpres: #previous ntp sync success
       rtcok = mrtc.setrtctime()
      else:
       tm = mrtc.getrtctime()
       if tm[0]<2020:
         print("RTC time is invalid")
         rtcok = False
       else:
        rtcok = mrtc.setsystime()
        misc.start_time = utime.time()
     if rtcok==False:
      print("RTC sync failed")
  except Exception as e:
   print("RTC init err:",e)

def wificonnect():
      try:
       import inc.unet as unet
       if settings.Settings['WifiClient']:
        print("Init wifi STA")
        try:
         unet.wifi_sta_mode(1)
        except:
         pass
        c = 15
        while (unet.wifi_sta_isconnected()==False) and (c>0):
         utime.sleep_ms(500)
         print('.')
         c-=1
        if (unet.wifi_sta_isconnected()==False):
         unet.wifi_sta_mode(2)
        c = 10
        while (unet.wifi_sta_isconnected()==False) and (c>0):
         utime.sleep_ms(500)
         print('.')
         c-=1
       else:
         unet.wifi_sta_disconnect(True)
      except:
       pass

def networkInit():
    try:
     import inc.unet as unet
     settings.ISWLAN, settings.ISLAN = unet.network_detect()
    except:
     settings.ISWLAN=False
     settings.ISLAN=False
    if settings.ISWLAN:
       wificonnect()
       if settings.Settings['WifiAP']>0:
        if settings.Settings['WifiAP']==1: #always
           unet.wifi_ap_mode()
        elif settings.Settings['WifiAP']==2: #if client notconnected
         if (unet.wifi_sta_isconnected()==False):
           unet.wifi_ap_mode()
         else:
           unet.wifi_ap_stop(True)
        elif settings.Settings['WifiAP']==4: #if lan notconnected
         if (unet.lan_isconnected()==False):
           unet.wifi_ap_mode()
         else:
           unet.wifi_ap_stop(True)
       else:
        unet.wifi_ap_stop(True)
    if settings.ISLAN:
     try:
      if settings.Settings["LANIF"] == -1:
       settings.Settings["LANIF"] = 1
     except:
      pass
     if settings.Settings["LANIF"]:
      try:
       print("Init LAN")
       unet.lan_init()
       c = 8
       while (unet.lan_isconnected()==False) and (c>0):
        utime.sleep_ms(500)
        print('-')
        c-=1
      except Exception as e:
       print("LAN init failed",e)
      if unet.lan_isconnected() == False and settings.Settings['LDHCP']==True:
       try:
        print("Force static IP")
        settings.Settings['LDHCP'] = False
        unet.lan_init(True)
        c = 5
        while (unet.lan_isconnected()==False) and (c>0):
         utime.sleep_ms(500)
         print('-')
         c-=1
       except:
        pass
    if unet.wifi_sta_isconnected() or unet.lan_isconnected():
     setclock() # set clock after network init to be nice with ntp
     print("http://"+ unet.get_ip() )
    else:
     print("No working network interface found")

def PluginInit():
 global fake
 tarr = []
 if fake:
  tarr = os.listdir(".")
 else:
  tarr = os.listdir("/")
 filenames = []
 for fname in tarr:
    if fname.startswith("_P"):
      filenames.append(fname)
 filenames.sort()
 for fname in filenames:
   tarr = [0,0,0]
   tarr[0] = fname
   with open(fname,"r") as fcont:
    for line in fcont:
     if "PLUGIN_ID" in line:
      tarr[1] = line[line.find("=")+1:].replace('"',"").strip()
     if "PLUGIN_NAME" in line:
      tarr[2] = line[line.find("=")+1:].replace('"',"").strip()
      break
   tarr[0] = tarr[0].replace(".py","")
   pglobals.deviceselector.append(tarr)
 if len(pglobals.deviceselector)<2:
  try:
   import inc.datacontainer
   pglobals.deviceselector = inc.datacontainer.plugincont #frozen modules
  except:
   pass
# print(pglobals.deviceselector)
 gc.collect()
 settings.loadtasks()

def CPluginInit():
 global fake
 tarr = []
 if fake:
  tarr = os.listdir(".")
 else:
  tarr = os.listdir("/")
 filenames = []
 for fname in tarr:
    if fname.startswith("_C"):
      filenames.append(fname)
 filenames.sort()
 for fname in filenames:
   tarr = [0,0,0]
   tarr[0] = fname
   with open(fname,"r") as fcont:
    for line in fcont:
     if "CONTROLLER_ID" in line:
      tarr[1] = line[line.find("=")+1:].replace('"',"").strip()
     if "CONTROLLER_NAME" in line:
      tarr[2] = line[line.find("=")+1:].replace('"',"").strip()
      break
   tarr[0] = tarr[0].replace(".py","")
   pglobals.controllerselector.append(tarr)
 if len(pglobals.controllerselector)<2:
  try:
   import inc.datacontainer
   pglobals.controllerselector = inc.datacontainer.controllercont #frozen modules
  except:
   pass
# print(pglobals.controllerselector)#debug
 gc.collect()
 try:
  settings.loadcontrollers()
 except Exception as e:
  print("Controller loading error",str(e))
 for x in range(0,len(settings.Tasks)):
  if (settings.Tasks[x]) and type(settings.Tasks[x]) is not bool: # device exists
   try:
    if (settings.Tasks[x].enabled): # device enabled
     settings.Tasks[x].plugin_init(None) # init plugin at startup
     for y in range(len(settings.Tasks[x].senddataenabled)):
       if (settings.Tasks[x].senddataenabled[y]):
        if (settings.Controllers[y]):
         if (settings.Controllers[y].enabled):
          settings.Tasks[x].controllercb[y] = settings.Controllers[y].senddata # assign controller callback to plugins that sends data
   except Exception as e:
    settings.Tasks[x].enabled = False
    misc.addLog(pglobals.LOG_LEVEL_ERROR,"Task " +str(x+1)+ " disabled! "+str(e))
 for y in range(0,len(settings.Controllers)):
   if (settings.Controllers[y]):
    try:
     if (settings.Controllers[y].enabled):
       settings.Controllers[y].controller_init(None) # init controller at startup
       settings.Controllers[y].setonmsgcallback(settings.callback_from_controllers) # set global msg callback for 2way comm
    except Exception as e:
       settings.Controllers[y].enabled = False
       misc.addLog(pglobals.LOG_LEVEL_ERROR,"Controller " +str(y+1)+ " disabled! "+str(e))

def NotifierInit():
 global fake
 tarr = []
 if fake:
  tarr = os.listdir(".")
 else:
  tarr = os.listdir("/")
 filenames = []
 for fname in tarr:
    if fname.startswith("_N"):
      filenames.append(fname)
 filenames.sort()
 for fname in filenames:
   tarr = [0,0,0]
   tarr[0] = fname
   with open(fname,"r") as fcont:
    for line in fcont:
     if "NPLUGIN_ID" in line:
      tarr[1] = line[line.find("=")+1:].replace('"',"").strip()
     if "NPLUGIN_NAME" in line:
      tarr[2] = line[line.find("=")+1:].replace('"',"").strip()
      break
   tarr[0] = tarr[0].replace(".py","")
   pglobals.notifierselector.append(tarr)
 if len(pglobals.notifierselector)<2:
  try:
   import inc.datacontainer
   pglobals.notifierselector = inc.datacontainer.notifiercont #frozen modules
  except:
   pass
# print(pglobals.deviceselector)#debug
 gc.collect()
 settings.loadnotifiers()

def RulesInit():
 rules = ""
 try:
  with open(pglobals.FILE_RULES,'r',encoding="utf8") as f:
   rules = f.read()
 except:
  pass
 try:
  if rules!="":
   print("Loading rules...")
   splitruletoevents(rules)
  rulesProcessing("System#Boot",pglobals.RULE_SYSTEM)
 except Exception as e:
  print("Rule loading error:",str(e))


async def main():
 global timer100ms, timer20ms, timer1s, timer2s, timer30s, init_ok, prevminute, fake
 ret = None
 amin = ""
 days = ['Mon','Tue',"Wed","Thu","Fri","Sat","Sun"]
 try:
      tf = open('www/dash.js',"r")
      doinit = False
 except OSError:
      doinit = True
 if doinit: #first run
       gc.collect()
       try:
        import inc.initdata as initdata
        initdata.run()
        del initdata
       except Exception as e:
        print("First init failed",e)
 try:
     gc.collect()
     settings.loadsettings()
     settings.loadadvsettings()
     hardwareInit(doinit)
     networkInit()
     PluginInit()
     CPluginInit()
     NotifierInit()
     RulesInit()
     init_ok = True
 except Exception as e:
     print("Init error, failing:",str(e))
     init_ok = False
 timer100ms = utime.ticks_ms()
 timer20ms  = timer100ms
 timer1s    = timer100ms
 timer2s    = timer100ms
 timer30s   = timer100ms
 print("Starting main loop")
 while init_ok:
    try:
        if fake:
         await asyncio.sleep(0.005)
        else:
         await asyncio.sleep_ms(5)
        if (timeoutReached(timer20ms)):
         run50timespersecond()
         timer20ms = utime.ticks_add(utime.ticks_ms(),20)
         if (timeoutReached(timer100ms)):
          run10timespersecond()
          timer100ms = utime.ticks_add(utime.ticks_ms(),100)
         if (timeoutReached(timer1s)):
          runoncepersecond()
          timer1s = utime.ticks_add(utime.ticks_ms(),1000)
          if (timeoutReached(timer30s)):
           await runon30seconds()
           timer30s = utime.ticks_add(utime.ticks_ms(),30000)
          ret = utime.localtime()
          amin = str('{:02}'.format(ret[4]))
          if (str(prevminute) != amin ):
            try:
             rulesProcessing(str('Clock#Time={},{:02}:{:02}'.format(days[int(ret[6])],ret[3],ret[4])),pglobals.RULE_CLOCK)
             prevminute = amin
            except Exception as e:
             print(e)
            gc.collect()
         if (timeoutReached(timer2s)):
          runon2seconds()
          timer2s = utime.ticks_add(utime.ticks_ms(),2000)
    except SystemExit:
        init_ok = False
    except KeyboardInterrupt:
        init_ok = False
    except EOFError:
        init_ok = False
    except Exception as e:
        print(e)
 print("Main loop ended")

loop = asyncio.get_event_loop()
loop.create_task(main())   #start main background loop
if fake:
 p = 8080
else:
 p = 80
loop.create_task(MicroWebSrv.serve(host='0.0.0.0', port=p)) #start web server loop
loop.run_forever() #continue forever
