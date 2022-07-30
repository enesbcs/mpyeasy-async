import webserver_global as ws
import pglobals
import gc
from commands import splitruletoevents
from web import awrite, parse_qs

async def handle_rules(request,response,chunk):
 ws.navMenuIndex=5
 ws.TXBuffer = ""
 ws.sendHeadandTail("TmplStd",ws._HEAD)
 if request.query is not None:
    responsearr = parse_qs(request.query)
 else:
    responsearr = []
 rules = ""
 saved = ws.arg("Submit",responsearr)
 if (saved):
  rules = ws.arg("rules",responsearr)
  try:
     with open(pglobals.FILE_RULES,'w') as f:
      f.write(rules)
  except:
     pass
  if len(rules)>0:
    splitruletoevents(rules)
 if rules=="":
    try:
     with open(pglobals.FILE_RULES,'r') as f:
      rules = f.read()
    except:
     pass
 ws.TXBuffer += "<form name = 'frmselect' method = 'post'><table class='normal'><TR><TH align='left'>Rules<tr><td><textarea name='rules' rows='30' wrap='off'>{0}</textarea>".format(rules)
 ws.addFormSeparator(2)
 ws.addSubmitButton()
 ws.TXBuffer += "</table></form>"

 ws.sendHeadandTail("TmplStd",ws._TAIL)
 await awrite(response,ws.TXBuffer,chunked=chunk,Force=True)
 ws.TXBuffer = ""
