import webserver_global as ws
import settings
from inc.unet import get_ip, get_rssi #import inc.unet as unet
import pglobals
from inc.misc import getuptime
from web import parse_qs, awrite, redirect, writeheaders, writefooters

async def handle_root(request,response,chunk):
 ws.navMenuIndex=0
 ws.TXBuffer = ""

 responsestr = ""
 if request.query is not None:
  responsearr = parse_qs(request.query)
 else:
  responsearr = []
 try:
  redir = settings.AdvSettings["startpage"]
 except:
  redir = "/"
 if redir != "/":
     return redirect(response,redir)

 writeheaders(response,chunked=False)
 ws.sendHeadandTail("TmplStd",ws._HEAD)

 try:
  ownip = response.get_extra_info('peername')[0]
 except:
  ownip = ""
 try:
  cmdline = ws.arg("cmd",responsearr).strip()
  if cmdline.startswith('reboot'):
     ws.sendHeadandTail("TmplStd",ws._TAIL)

  if len(cmdline)>0:
   from commands import doExecuteCommand
   responsestr = str(doExecuteCommand(cmdline))
 except:
  pass

 if len(responsestr)>0:
   ws.TXBuffer += "<P>{0}<p>".format(responsestr)

 ws.TXBuffer += "<form><table class='normal'><tr><TH style='width:150px;' align='left'>System Info<TH align='left'>Value<TR><TD>Unit:<TD>"
 ws.TXBuffer += str(settings.Settings["Unit"])
 ws.TXBuffer += "<TR><TD>Uptime:<TD>" + str(getuptime(1))
 if await awrite(response,ws.TXBuffer,chunked=chunk):
  ws.TXBuffer = ""

# try:
#  ws.TXBuffer += "<TR><TD>Free Mem:<TD>" + str( int(esp_os.get_memory()['f'] /1024) ) + " kB"
# except:
#  pass
 ws.TXBuffer += "<TR><TD>IP:<TD>" + str( get_ip(nm="",clip=ownip) )
 ws.TXBuffer += "<TR><TD>Wifi RSSI:<TD>" + str(get_rssi())
 ws.TXBuffer += '<tr><td>Build<td>' + str(pglobals.PROGNAME) + " " + str(pglobals.PROGVER)
 ws.TXBuffer += "<TR><TD><TD>"
 ws.addButton("sysinfo", "More info")
 ws.TXBuffer += "</table><BR>"
 if len(settings.nodelist)>0:
   ws.TXBuffer += "<BR><table class='multirow'><TR><TH>Node List<TH>Name<TH>Build<TH>Type<TH>IP<TH>Age"
   for n in settings.nodelist:
    ws.TXBuffer += "<TR><TD>Unit "+str(n["unitno"])+"<TD>"+str(n["name"])+"<TD>"+str(n["build"])+"<TD>"
    ntype = ""
    if int(n["type"])==pglobals.NODE_TYPE_ID_ESP_EASY_STD:
     ntype = "ESP Easy"
    elif int(n["type"])==pglobals.NODE_TYPE_ID_ESP_EASYM_STD:
     ntype = "ESP Easy Mega"
    elif int(n["type"])==pglobals.NODE_TYPE_ID_ESP_EASY32_STD:
     ntype = "ESP Easy32"
    elif int(n["type"])==pglobals.NODE_TYPE_ID_ARDUINO_EASY_STD:
     ntype = "Arduino Easy"
    elif int(n["type"])==pglobals.NODE_TYPE_ID_NANO_EASY_STD:
     ntype = "Nano Easy"
    elif int(n["type"])==pglobals.NODE_TYPE_ID_RPI_EASY_STD:
     ntype = "RPI Easy"
    ws.TXBuffer += ntype+"<TD>"
    waddr = str(n["ip"])
    if str(n["port"]) != "" and str(n["port"]) != "0" and str(n["port"]) != "80":
     waddr += ":" + str(n["port"])
    ws.addWideButton("http://"+waddr, waddr, "")
    ws.TXBuffer += "<TD>"+str(n["age"])
   ws.TXBuffer += "</table></form>"

 if len(settings.p2plist)>0:
  try:
   ws.TXBuffer += "<BR><table class='multirow'><TR><TH>Protocol<TH>P2P node number<TH>Name<TH>Build<TH>Type<TH>MAC<TH>RSSI<TH>Last seen<TH>Capabilities"
   for n in settings.p2plist:
    hstr = str(n["protocol"])
    if hstr=="ESPNOW":
     hstr = "<a href='espnow'>"+hstr+"</a>"
    ws.TXBuffer += "<TR><TD>"+hstr+"<TD>Unit "+str(n["unitno"])+"<TD>"+str(n["name"])+"<TD>"+str(n["build"])+"<TD>"
    ntype = "Unknown"
    if int(n["type"])==pglobals.NODE_TYPE_ID_ESP_EASY_STD:
     ntype = "ESP Easy"
    elif int(n["type"])==pglobals.NODE_TYPE_ID_ESP_EASYM_STD:
     ntype = "ESP Easy Mega"
    elif int(n["type"])==pglobals.NODE_TYPE_ID_ESP_EASY32_STD:
     ntype = "ESP Easy32"
    elif int(n["type"])==pglobals.NODE_TYPE_ID_ARDUINO_EASY_STD:
     ntype = "Arduino Easy"
    elif int(n["type"])==pglobals.NODE_TYPE_ID_NANO_EASY_STD:
     ntype = "Nano Easy"
    elif int(n["type"])==pglobals.NODE_TYPE_ID_RPI_EASY_STD:
     ntype = "RPI Easy"
    elif int(n["type"])==pglobals.NODE_TYPE_ID_ATMEGA_EASY_LORA:
     ntype = "LoRa32u4"
    ws.TXBuffer += ntype
    ws.TXBuffer += "<TD>"+str(n["mac"])
    ws.TXBuffer += "<TD>"+str(n["lastrssi"])
    ldt = n["lastseen"]
    lstr = ""
    try:
     lstr = '{:04}-{:02}-{:02} {:02}:{:02}:{:02}'.format(ldt[0],ldt[1],ldt[2],ldt[3],ldt[4],ldt[5])
    except:
     lstr = str(ldt)
    ws.TXBuffer += "<TD>"+lstr
    wm = int(n["cap"])
    wms = ""
    if (wm & 1)==1:
     wms = "SEND "
    if (wm & 2)==2:
     wms += "RECEIVE "
    ws.TXBuffer += "<TD>"+wms
   ws.TXBuffer += "</table></form>"
  except Exception as e:
   pass

 ws.sendHeadandTail("TmplStd",ws._TAIL)
 await awrite(response,ws.TXBuffer,chunked=chunk,Force=True)
 await writefooters(response,chunked=False)
 ws.TXBuffer = ""
