import webserver_global as ws
import commands
from web import awrite

async def handle_sysvars(request,response,chunk):
 ws.navMenuIndex=7
 ws.TXBuffer = ""
 ws.sendHeadandTail("TmplStd",ws._HEAD)
 ws.TXBuffer += "<table class='normal'><TR><TH align='left'>System Variables<TH align='left'>Normal"
 for sv in commands.SysVars:
  ws.TXBuffer += "<TR><TD>%" + sv + "%</TD><TD>"
  ws.TXBuffer += str(commands.getglobalvar(sv)) + "</TD></TR>"
  if await awrite(response,ws.TXBuffer,chunked=chunk):
   ws.TXBuffer = ""
 conversions = [ "%c_m2day%(%uptime%)", "%c_m2dh%(%uptime%)", "%c_m2dhm%(%uptime%)" ]
 for sv in conversions:
  try:
   ws.TXBuffer += "<TR><TD>" + sv + "</TD><TD>"
   ws.TXBuffer += str(commands.parseruleline(sv)[0]) + "</TD></TR>"
  except:
   pass
  if await awrite(response,ws.TXBuffer,chunked=chunk):
   ws.TXBuffer = ""
 ws.TXBuffer += "</table></form>"
 ws.sendHeadandTail("TmplStd",ws._TAIL)
 await awrite(response,ws.TXBuffer,chunked=chunk,Force=True)
 ws.TXBuffer = ""
