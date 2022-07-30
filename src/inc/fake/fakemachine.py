from pynput.keyboard import Key,Listener,Controller # pip install pynput
import subprocess

gpios = ['0','1','2','3','4','5','6','7','8','9',Key.up, Key.down, Key.left, Key.right, Key.enter, Key.caps_lock, Key.num_lock]
gpiostate = []
gpioirqon = []
gpioirqoff = []

def reset():
    pass

def soft_reset():
    pass

def freq(hz=None):
    return 2000000

def unique_id():
    return "Fake Machine Unit"

def CleanUp():
    global listener    
    try:
        print("CTRL aborted keyboardlistener")#debug
        listener.stop()
    except Exception as e:
        print(e)

def compareCodes(code1,code2):
    if type(code1) == type(code2):
       return (code1==code2)
    else:
       try:
        c1 = code1.char
       except:
        c1 = str(code1)
       try:
        c2 = code2.char
       except:
        c2 = str(code2)        
       return (c1==c2)
   
def getCapsState():  
    cs = 0
    try:
     capsStatus = subprocess.getoutput("xset q | grep Caps | tr -s ' ' | cut -d ' ' -f 5")
     if capsStatus == 'on':
      cs = 1
    except:
     cs = 0
    return cs

def getNumState():  
    ns = 0
    try:
     numStatus = subprocess.getoutput("xset q | grep Caps | tr -s ' ' | cut -d ' ' -f 9")
     if numStatus == 'on':
      ns = 1
    except:
     ns = 0
    return ns

def getPinNum(key):
    global gpios
    vi = None
    for g in range(len(gpios)):
        if compareCodes(gpios[g],key):
           return g
    return vi

def keypressed(key):
    global gpios, gpiostate, gpioirqon
    if key==Key.ctrl:
       CleanUp()
    pn = getPinNum(key)
    if pn is not None:
     try:
      if compareCodes(key, Key.caps_lock):
       gpiostate[pn] = getCapsState()
      elif compareCodes(key, Key.num_lock):
       gpiostate[pn] = getNumState()
      else:
       gpiostate[pn] = 1
      if gpioirqon[pn] is not None:
        try:
         gpioirqon[pn](pn)
        except:
         pass         
     except:
      pass
    
def keyreleased(key):
    global gpios, gpiostate, gpioirqoff

    pn = getPinNum(key)
    if pn is not None:
     try:
      if compareCodes(key, Key.caps_lock):
       gpiostate[pn] = getCapsState()
      elif compareCodes(key, Key.num_lock):
       gpiostate[pn] = getNumState()
      else:
       gpiostate[pn] = 0
      if gpioirqoff[pn] is not None:
        try:
         gpioirqoff[pn](pn)
        except:
         pass         
     except:
      pass    
#Fake Machine
    

class Pin():
 IN=1
 OUT=3
 PULL_UP=2
 PULL_DOWN=1
 IRQ_FALLING=2
 IRQ_RISING=1
 
 def __init__(self,id, mode=-1, pull=-1, value=None, drive=0, alt=-1):
     self.pin = id
     self.initialized = False
     self.init(mode, pull, value, drive, alt)
 
 def init(self,mode=-1, pull=-1, value=None, drive=0, alt=-1):
     global gpios
     if self.pin < len(gpios):
        self.initialized = True
        if value is not None:
           self.value(value)
     else:
        self.initialized = False

 def value(self,val=None):
     global gpiostate, gpios, keyctrl
     if self.initialized:
        if val==None:
         return gpiostate[self.pin]
        else:
         if gpios[self.pin] == Key.caps_lock or gpios[self.pin] == Key.num_lock:
            if int(val) != gpiostate[self.pin]:
             keyctrl.press(gpios[self.pin])
             keyctrl.release(gpios[self.pin])
             if val==0:
              if gpioirqoff[self.pin] is not None:
                try:
                 gpioirqoff[self.pin](self.pin)
                except:
                 pass
             else:
              if gpioirqon[self.pin] is not None:
                try:
                 gpioirqon[self.pin](self.pin)
                except:
                 pass
         gpiostate[self.pin] = val

 def on(self):
     self.value(1)
     
 def off(self):
     self.value(0)

 def irq(self,handler=None, trigger=3, priority=1, wake=None, hard=False):
     global gpioirqon, gpioirqoff
     if self.initialized:
      if (trigger & Pin.IRQ_FALLING) > 0:
        gpioirqoff[self.pin] = handler
      if (trigger & Pin.IRQ_RISING) > 0:
        gpioirqon[self.pin] = handler        
         

class PWM():
 def __init__(self, dest, freq, duty):
     init(freq, duty,0)
     
 def init (self, freq, duty_u16, duty_ns):
     pass
 
 def deinit():
     pass
 
 def freq(value=None):
     pass
 
class I2C():
 def __init__(self, id, scl, sda, freq=400000):
     pass

class SPI():
 def __init__(self, baudrate=500000, polarity=0, phase=0, bits=8, firstbit=1, sck=None, mosi=None, miso=None):
     pass

class UART():
 def __init__(self, id, baudrate=9600, bits=8, parity=None, stop=1, timeout=0):
     pass

#Global Init
if len(gpiostate)<1:    
 for g in range(len(gpios)):
    gpiostate.append(0)
    if compareCodes(gpios[g], Key.caps_lock):
       gpiostate[g] = getCapsState()
    elif compareCodes(gpios[g], Key.num_lock):
       gpiostate[g] = getNumState()   
    gpioirqon.append(None)
    gpioirqoff.append(None)

keyctrl = Controller()
listener = Listener(on_press=keypressed, on_release=keyreleased,suppress=False)
listener.start()
