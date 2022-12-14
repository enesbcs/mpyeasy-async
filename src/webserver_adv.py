import webserver_global as ws
import settings
from web import awrite, parse_qs

async def handle_adv(request,response,chunk):
 ws.navMenuIndex=7
 ws.TXBuffer = ""
 if request.query is not None:
   responsearr = parse_qs(request.query)
 else:
  responsearr = []

 saved = ws.arg("Submit",responsearr)
 if (saved):
   settings.AdvSettings["webloglevel"]  = int(ws.arg("webloglevel",responsearr))
   settings.AdvSettings["consoleloglevel"]  = int(ws.arg("consoleloglevel",responsearr))
   settings.AdvSettings["usentp"]  = (ws.arg("usentp",responsearr) == "on")
   settings.AdvSettings["ntpserver"]  = ws.arg("ntpserver",responsearr)
   settings.AdvSettings["timezone"]  = int(ws.arg("timezone",responsearr))
   try:
    settings.AdvSettings["rtci2c"] = int(ws.arg("rtci2c",responsearr))
    if settings.AdvSettings["rtci2c"]>=0:
     settings.AdvSettings["extrtc"] = int(ws.arg("extrtc",responsearr))
    if settings.AdvSettings["rtcaddr"]>=0:
     settings.AdvSettings["rtcaddr"] = int(ws.arg("rtcaddr",responsearr))
   except:
    settings.AdvSettings["extrtc"] = 0
    settings.AdvSettings["rtci2c"] = 0
   try:
    settings.AdvSettings["dangerouspins"] = ws.arg("dangerouspins",responsearr)
   except:
    settings.AdvSettings["dangerouspins"] = False
   try:
    settings.AdvSettings["Latitude"]  = float(ws.arg("latitude",responsearr))
    settings.AdvSettings["Longitude"] = float(ws.arg("longitude",responsearr))
   except:
    settings.AdvSettings["Latitude"]  = 0
    settings.AdvSettings["Longitude"] = 0
   try:
    settings.AdvSettings["startpage"]  = str(ws.arg("startpage",responsearr))
   except:
    settings.AdvSettings["startpage"]  = "/"    
   settings.saveadvsettings()

 ws.sendHeadandTail("TmplStd",ws._HEAD)

 ws.TXBuffer += "<form  method='post'><table class='normal'>"
 ws.addFormHeader("Advanced Settings")
 ws.addFormSubHeader("Log Settings")
 if await awrite(response,ws.TXBuffer,chunked=chunk):
  ws.TXBuffer = ""
 ws.addFormLogLevelSelect("Console log Level","consoleloglevel", settings.AdvSettings["consoleloglevel"])
 ws.addFormLogLevelSelect("Web log Level",    "webloglevel",     settings.AdvSettings["webloglevel"])
 ws.addFormSubHeader("Time Settings")
 ws.addFormCheckBox("Enable NTP","usentp",settings.AdvSettings["usentp"])
 ws.addFormTextBox( "NTP server name", "ntpserver", settings.AdvSettings["ntpserver"], 100)
 ws.addFormNumericBox("Timezone offset", "timezone", settings.AdvSettings["timezone"], -720, 840)
 ws.addUnit("min")
 try:
  extrtc = settings.AdvSettings["extrtc"]
 except:
  settings.AdvSettings["extrtc"] = 0
  extrtc = 0
 options = ["Disable","DS1307","DS3231","PCF8523"]
 optionvalues = [0,1307,3231,8523]
 ws.addFormSelector("External RTC type","extrtc",len(optionvalues),options,optionvalues,None,extrtc)
 try:
    import inc.libhw as libhw
    options = libhw.geti2clist()
 except:
    options = []
 try:
  rtci2c = settings.AdvSettings["rtci2c"]
 except:
  rtci2c = 0
  settings.AdvSettings["rtci2c"] = 0
 ws.addHtml("<tr><td>RTC I2C line:<td>")
 ws.addSelector_Head("rtci2c",True)
 for d in range(len(options)):
    ws.addSelector_Item("I2C"+str(options[d]),options[d],(rtci2c==options[d]),False)
 ws.addSelector_Foot()
 try:
  rtcaddr = settings.AdvSettings["rtcaddr"]
 except:
  rtcaddr = 0
  settings.AdvSettings["rtcaddr"] = 0
 options = ["0","0x68","0x51"]
 optionvalues = [0,0x68,0x51]
 ws.addFormSelector("RTC I2C address","rtcaddr",len(optionvalues),options,optionvalues,None,rtcaddr)
 res = ""
 try:
  if settings.AdvSettings['extrtc']>0 and settings.AdvSettings['rtci2c']>=0:
     import inc.mrtc as mrtc
     try:
      import inc.libhw as libhw
     except:
       pass
     if mrtc.I2C_RTC is None:
      if settings.AdvSettings['rtci2c']==0:
       rtcok = mrtc.rtcinit(settings.AdvSettings['extrtc'],libhw.i2c0,settings.AdvSettings["rtcaddr"])
      elif settings.AdvSettings['rtci2c']==1:
       rtcok = mrtc.rtcinit(settings.AdvSettings['extrtc'],libhw.i2c1,settings.AdvSettings["rtcaddr"])
     ret = mrtc.getrtctime()
     res = '{:04}-{:02}-{:02} {:02}:{:02}:{:02}'.format(ret[0],ret[1],ret[2],ret[4],ret[5],ret[6])
 except Exception as e:
  res = "RTC not available "+str(e)
 if settings.AdvSettings['extrtc']>0:
    ws.addFormNote(res)
 if await awrite(response,ws.TXBuffer,chunked=chunk):
  ws.TXBuffer = ""
 ws.addFormSubHeader("Misc Settings")
 try:
  dpins = settings.AdvSettings["dangerouspins"]
 except:
  dpins = False
 ws.addFormCheckBox("Show dangerous pins","dangerouspins",dpins)

 try:
  sp = settings.AdvSettings["startpage"]
 except:
  sp = "/"
 ws.addFormTextBox("Start page", "startpage", sp,64)
 if await awrite(response,ws.TXBuffer,chunked=chunk):
  ws.TXBuffer = ""

 ws.addFormSubHeader("Location Settings")
 try:
   lat = settings.AdvSettings["Latitude"]
   lon = settings.AdvSettings["Longitude"]
 except:
   lat = 0
   lon = 0
 ws.addFormFloatNumberBox("Latitude", "latitude", lat , -90.0, 90.0)
 ws.addUnit("&deg;")
 ws.addFormFloatNumberBox("Longitude", "longitude", lon, -180.0, 180.0)
 ws.addUnit("&deg;")

 ws.addFormSeparator(2)
 ws.TXBuffer += "<TR><TD style='width:150px;' align='left'><TD>"
 ws.addSubmitButton()
 ws.TXBuffer += "<input type='hidden' name='edit' value='1'>"
 ws.TXBuffer += "</table></form>"

 ws.sendHeadandTail("TmplStd",ws._TAIL)
 await awrite(response,ws.TXBuffer,chunked=chunk,Force=True)
 ws.TXBuffer = ""
