import settings
if settings.HWType==1:#esp32
   from inc.esp32.lib_gpiohelper import *
elif settings.HWType==2:#rp2
   from inc.rp2.lib_gpiohelper import *
else:
   from inc.fake.lib_gpiohelper import *
