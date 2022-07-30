import webserver_global as ws
from commands import doExecuteCommand
from web import awrite, parse_qs
import gc

async def handle_command(request,response,chunk):
 ws.navMenuIndex=0
 ws.TXBuffer = ""
 responsestr = ""
 if request.query is not None:
   responsearr = parse_qs(request.query)
 else:
  responsearr = []

 ws.sendHeadandTail("TmplStd",ws._HEAD)
 try:
  cmdline = ws.arg("cmd",responsearr).strip()
  if cmdline.startswith('reboot'):
     ws.sendHeadandTail("TmplStd",ws._TAIL)

  if len(cmdline)>0:
   responsestr = str(doExecuteCommand(cmdline))
 except:
  pass

 if len(responsestr)>0:
   ws.TXBuffer += "<P>{0}<p>".format(responsestr)
 if responsestr == False:
  ws.TXBuffer += "FAILED"
 ws.sendHeadandTail("TmplStd",ws._TAIL)
 await awrite(response,ws.TXBuffer,chunked=chunk,Force=True)
 ws.TXBuffer = ""
