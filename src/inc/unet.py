import settings

if settings.HWType<0:
    from inc.libhw import gethwtype
    settings.HWType = gethwtype()
if settings.HWType==1:#esp32
   from inc.esp32.unet import *
elif settings.HWType==2:#rp2
   from inc.rp2.unet import *
else:
   from inc.fake.unet import *
