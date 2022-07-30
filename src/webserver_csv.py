import webserver_global as ws
import settings
from web import awrite, parse_qs

async def handle_csv(request,response,chunk):
 ws.navMenuIndex=7
 ws.TXBuffer = ""
 if request.query is not None:
  responsearr = parse_qs(request.query)
 else:
  responsearr = []

 tasknrstr = ws.arg("tasknr",responsearr).strip()
 sc = -1
 if (len(tasknrstr)>0):
  try:
   sc = int(tasknrstr)
  except:
   sc = -1
 tasknrstr = ws.arg("tasks",responsearr).strip()
 valnr = ws.arg("valnr",responsearr)
 try:
  tv = int(valnr)
 except:
  tv = -1
 rheader = (ws.arg("header",responsearr)!="0")

 if sc>=0:
  if sc<len(settings.Tasks) and settings.Tasks[sc] != False and settings.Tasks[sc].enabled:
   if tv>-1:
    if tv>=settings.Tasks[sc].valuecount:#nono
     await awrite(response,ws.TXBuffer,chunked=chunk,Force=True)
     ws.TXBuffer = ""
     return
    if rheader:
     ws.TXBuffer += str(settings.Tasks[sc].valuenames[tv])+';\n'
    if str(settings.Tasks[sc].uservar[tv])=="":
      ws.TXBuffer += '""'
    else:
      if str(settings.Tasks[sc].decimals[tv]) == "-1":
       ival = '"'+ str(settings.Tasks[sc].uservar[tv]) + '"'
      else:
       try:
        ival = float(settings.Tasks[sc].uservar[tv])
       except:
        ival = '"'+ str(settings.Tasks[sc].uservar[tv]) + '"'
      ws.TXBuffer += str(ival)
    ws.TXBuffer += ";\n"
   else:
    if rheader:
     for tv in range(0,settings.Tasks[sc].valuecount):
      ws.TXBuffer += str(settings.Tasks[sc].valuenames[tv])+';'
     ws.TXBuffer += "\n"
    for tv in range(0,settings.Tasks[sc].valuecount):
     if str(settings.Tasks[sc].uservar[tv])=="":
      ws.TXBuffer += '""'
     else:
      if str(settings.Tasks[sc].decimals[tv]) == "-1":
       ival = '"'+ str(settings.Tasks[sc].uservar[tv]) + '"'
      else:
       try:
        ival = float(settings.Tasks[sc].uservar[tv])
       except:
        ival = '"'+ str(settings.Tasks[sc].uservar[tv]) + '"'
      ws.TXBuffer += str(ival)
     ws.TXBuffer += ";"
    ws.TXBuffer += "\n"
 elif "_" in tasknrstr:
  tia = tasknrstr.split(",")
  for ti in tia:
   try:
    t = ti.split("_")
    sc = int(t[0])
    tv = int(t[1])
    if sc<len(settings.Tasks) and settings.Tasks[sc] != False and settings.Tasks[sc].enabled:
     if tv>-1:
      if tv>=settings.Tasks[sc].valuecount:#nono
        ws.TXBuffer += '"";'
        continue
      if str(settings.Tasks[sc].uservar[tv])=="":
        ws.TXBuffer += '""'
      else:
        if str(settings.Tasks[sc].decimals[tv]) == "-1":
         ival = '"'+ str(settings.Tasks[sc].uservar[tv]) + '"'
        else:
         try:
          ival = float(settings.Tasks[sc].uservar[tv])
         except:
          ival = '"'+ str(settings.Tasks[sc].uservar[tv]) + '"'
        ws.TXBuffer += str(ival)
      ws.TXBuffer += ";"
     else:
      ws.TXBuffer += '"";'
    else:
      ws.TXBuffer += '"";'
   except Exception as e:
    pass
 await awrite(response,ws.TXBuffer,chunked=chunk,Force=True)
 ws.TXBuffer = ""

