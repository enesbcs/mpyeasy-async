import webserver_global as ws
import settings
import inc.unet as unet
import pglobals
import gc
import inc.misc as misc
import sys
import inc.libhw as libhw
try:
 import uos
except:
 import os as uos
from web import awrite, parse_qs

async def handle_sysinfo(request,response,chunk):
 ws.navMenuIndex=7
 ws.TXBuffer = ""
 ws.sendHeadandTail("TmplStd",ws._HEAD)
 ws.TXBuffer += "<table class='normal'><TR><TH style='width:150px;' align='left'>System Info<TH align='left'>"
 ws.TXBuffer += "<TR><TD>Unit<TD>"
 ws.TXBuffer += str(settings.Settings["Unit"])
 ws.TXBuffer += "<TR><TD>Local Time<TD>" + misc.strtime(0) #Local Time: (2000, 1, 1, 0, 45, 20, 5, 1)
 ws.TXBuffer += "<TR><TD>Uptime<TD>" + str(misc.getuptime(1))
 if await awrite(response,ws.TXBuffer,chunked=chunk):
  ws.TXBuffer = ""
 ws.TXBuffer += "<TR><TD>Frequency<TD>" + str( int(libhw.getfreq() /1000000)) +" Mhz"
# try:
#  ws.TXBuffer += "<TR><TD>Flash<TD>" + str( int(esp_os.getstorage() /1024)) + " kB"
# except:
#  pass
 try:
  ws.TXBuffer += "<TR><TD>Memory<TD>" + str( int(libhw.get_memory()['t'] /1024) ) + " kB"
 except:
  pass
 try:
  ws.TXBuffer += "<TR><TD>Free Mem<TD>" + str( int(libhw.get_memory()['f'] /1024) ) + " kB"
 except:
  pass
 if await awrite(response,ws.TXBuffer,chunked=chunk):
  ws.TXBuffer = ""
 try:
  uver = uos.uname()
  uver2 = 'uPython '+ str(uver.version)
  umach = str(uver.machine)
 except:
  uver2 = ""
  umach = ""
 if umach != "":
  ws.TXBuffer += "<TR><TD>Device<TD>" + str( umach )
 ws.TXBuffer += '<tr><td>Platform<td>' +sys.platform
 ws.TXBuffer += "<TR><TD>Wifi RSSI<TD>" + str(unet.get_rssi())
 ws.TXBuffer += '<tr><td>SSID<td>'+str( unet.get_ssid())
 ws.TXBuffer += '<tr><td>STA IP<td>'+ str( unet.get_ip("STA") )
 ws.TXBuffer += '<tr><td>STA MAC<td>'+ str( unet.get_mac("STA") )
 ws.TXBuffer += '<tr><td>AP IP<td>'+ str( unet.get_ip("AP") )
 ws.TXBuffer += '<tr><td>AP MAC<td>'+ str( unet.get_mac("AP") )
 ws.TXBuffer += '<tr><td>LAN IP<td>'+ str( unet.get_ip("LAN") )
 ws.TXBuffer += '<tr><td>LAN MAC<td>'+ str( unet.get_mac("LAN") ) 
 if await awrite(response,ws.TXBuffer,chunked=chunk):
  ws.TXBuffer = ""
 ws.TXBuffer += '<tr><td>Build<td>' + str(pglobals.PROGNAME) + " " + str(pglobals.PROGVER)
 ws.TXBuffer += '<tr><td>Libraries<td>Python ' + sys.version.replace('\n','<br>')+" "+uver2
 ws.TXBuffer += '<tr><td>Plugins<td>'+str(len(pglobals.deviceselector)-1)
 ws.TXBuffer += "</tr></table>"
 try:
  import inc.esp32.lib_part as PartMgr
  pm = PartMgr.partmgr()
  pl = pm.getparts()
 except:
  pl = []
 if len(pl)>0:
  try:
   pr = pm.getrunningpart()[4]
   pb = pm.getbootpart()[4]
  except:
   pr = ""
   pb = ""
  ws.TXBuffer += "<p><table class='normal'><tr><th>Partition</th><th>Start address</th><th>Size</th><th>Flags</th></tr>"
  for p in pl:
   prf = ""
   if pr==p[4]:
    prf = "Running "
   if pb==p[4]:
    prf += "Boot "
   ws.TXBuffer += "<tr><td>{0}</td><td>0x{1:07x}</td><td>{2}</td><td>{3}</td></tr>".format(p[4],p[2],p[3],prf)
  ws.TXBuffer += "</table>"
 ws.sendHeadandTail("TmplStd",ws._TAIL)
 await awrite(response,ws.TXBuffer,chunked=chunk,Force=True)
 ws.TXBuffer = ""
