import settings
if settings.HWType==1:#esp32
   from inc.esp32.lib_plat import *
elif settings.HWType==2:#rp2
   from inc.rp2.lib_plat import *
else:
   from inc.fake.lib_plat import *
