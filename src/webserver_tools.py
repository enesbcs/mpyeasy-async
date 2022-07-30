import webserver_global as ws
from web import awrite, parse_qs
from commands import CommandQueue
import settings

async def handle_tools(request,response,chunk):
 ws.navMenuIndex=7
 ws.TXBuffer = ""
 if request.query is not None:
  responsearr = parse_qs(request.query)
 else:
  responsearr = []
 webrequest = ws.arg("cmd",responsearr)
 ws.sendHeadandTail("TmplStd",ws._HEAD)
 ws.TXBuffer += "<form><table class='normal'>"
 ws.addFormHeader("Tools")
 ws.addFormSubHeader("Command")
 ws.TXBuffer += "<TR><TD style='width: 280px'><input class='wide' type='text' name='cmd' value='{0}'><TD>".format(webrequest)
 ws.addSubmitButton()
 if await awrite(response,ws.TXBuffer,chunked=chunk):
  ws.TXBuffer = ""
 responsestr = ""
 if webrequest.startswith('reboot'):
     ws.sendHeadandTail("TmplStd",ws._TAIL)
     await awrite(response,ws.TXBuffer,chunked=chunk,Force=True)
     ws.TXBuffer = ""
     return
 try:
  if len(webrequest)>0:
   import commands
   CommandQueue.append(webrequest) #   responsestr = str(commands.doExecuteCommand(webrequest))
 except:
  pass
 if len(webrequest)>0:
  try:
   import inc.misc as misc
   ws.TXBuffer += "<TR><TD colspan='2'>Command Output<BR><textarea readonly rows='10' wrap='on'>"
   ws.TXBuffer += str(responsestr)
   lc = len(misc.SystemLog)
   if lc>5:
    ls = lc-5
   else:
    ls = 0
   for l in range(ls,lc):
    ws.TXBuffer += '\r\n'+str(misc.SystemLog[l]["t"])+" : "+ str(misc.SystemLog[l]["l"])
   ws.TXBuffer += "</textarea>"
  except Exception as e:
   print(str(e))
 if await awrite(response,ws.TXBuffer,chunked=chunk):
  ws.TXBuffer = ""
 ws.addFormSubHeader("System")

 ws.TXBuffer += "<tr><td height=30>"
 ws.TXBuffer += "<a class='button link wide' onclick="
 ws.TXBuffer += '"'
 ws.TXBuffer += "return confirm('Do you really want to Reboot device?')"
 ws.TXBuffer += '"'
 ws.TXBuffer += " href='/?cmd=reboot'>Reboot</a>"
 ws.TXBuffer += "<TD>"
 ws.TXBuffer += "Reboot System"

 ws.TXBuffer += "<tr><td height=30>"
 ws.addWideButton("log", "Log", "")
 ws.TXBuffer += "<TD>"
 ws.TXBuffer += "Open log output"

 ws.TXBuffer += "<tr><td height=30>"
 ws.addWideButton("sysinfo", "Info", "")
 ws.TXBuffer += "<TD>"
 ws.TXBuffer += "Open system info page"

 ws.TXBuffer += "<tr><td height=30>"
 ws.addWideButton("advanced", "Advanced", "")
 ws.TXBuffer += "<TD>"
 ws.TXBuffer += "Open advanced settings"
 if await awrite(response,ws.TXBuffer,chunked=chunk):
  ws.TXBuffer = ""

 ws.TXBuffer += "<tr><td height=30>"
 ws.addWideButton("sysvars", "System Variables", "")
 ws.TXBuffer += "<TD>"
 ws.TXBuffer += "Show all system variables"

 if False: #debug #untested #todo
  ws.TXBuffer += "<tr><td height=30>"
  ws.addWideButton("update", "OTA Update", "")
  ws.TXBuffer += "<TD>"
  ws.TXBuffer += "OTA update"

 ws.TXBuffer += "<tr><td height=30>"
 ws.TXBuffer += "<a class='button link wide red' onclick="
 ws.TXBuffer += '"'
 ws.TXBuffer += "return confirm('Do you really want to Reset/Erase all settings?')"
 ws.TXBuffer += '"'
 ws.TXBuffer += " href='/?cmd=reset'>Reset device settings</a>"
 ws.TXBuffer += "<TD>"
 ws.TXBuffer += "Erase all setting files"
 if await awrite(response,ws.TXBuffer,chunked=chunk):
  ws.TXBuffer = ""

 ws.addFormSubHeader("Scan")

 if settings.ISWLAN:
  ws.TXBuffer += "<tr><td height=30>"
  ws.addWideButton("wifiscanner", "WiFi Scan", "")
  ws.TXBuffer += "<TD>"
  ws.TXBuffer += "Scan WiFi AP's"

 ws.TXBuffer += "<tr><td height=30>"
 ws.addWideButton("blescanner", "BLE Scan", "")
 ws.TXBuffer += "<TD>"
 ws.TXBuffer += "Scan nearby BLE devices"

 ws.TXBuffer += "<tr><td height=30>"
 ws.addWideButton("i2cscanner", "I2C Scan", "")
 ws.TXBuffer += "<TD>"
 ws.TXBuffer += "Scan I2C devices"

 ws.TXBuffer += "</table></form>"

 ws.sendHeadandTail("TmplStd",ws._TAIL)
 await awrite(response,ws.TXBuffer,chunked=chunk,Force=True)
 ws.TXBuffer = ""
