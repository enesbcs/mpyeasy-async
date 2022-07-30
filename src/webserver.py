#mPyEasy WebServer
import web
import inc.misc as misc
import pglobals
import gc

MicroWebSrv = web.App()

@MicroWebSrv.route("/defaultu.css")
async def file_defcss(request,response):
      await web.send_file(response,"www/defaultu.css",content_type="text/css")
      await web.writefooters(response)

@MicroWebSrv.route("/favicon.ico")
async def file_defcss(request,response):
      await web.send_file(response,"www/favicon.ico",content_type="image/x-icon")
      await web.writefooters(response)

@MicroWebSrv.route("/dash.css")
async def file_dashcss(request):
      await web.send_file(response,"www/dash.css",content_type="text/css")
      await web.writefooters(response)

@MicroWebSrv.route("/dash.js")
async def file_dashjs(request):
      await web.send_file(response,"www/dash.js",content_type="text/javascript")
      await web.writefooters(response)

@MicroWebSrv.route('/')
@MicroWebSrv.route('/generate_204')
async def handle_root(request, response):
 try:
  gc.collect()
  import webserver_root
  await webserver_root.handle_root(request,response,False)
  del webserver_root
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver root error: "+str(e))

@MicroWebSrv.route('/config',methods=['GET','POST'])
async def handle_config(request,response):
 try:
  gc.collect()
  import webserver_config
  web.writeheaders(response,chunked=False) #200 ok
  await webserver_config.handle_config(request,response,False)
  await web.writefooters(response,chunked=False) #close
  del webserver_config
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver config error: "+str(e))

@MicroWebSrv.route('/controllers',methods=['GET','POST'])
async def handle_controllers(request,response):
 try:
  gc.collect()
  import webserver_contr
  web.writeheaders(response,chunked=False) #200 ok
  await webserver_contr.handle_controllers(request,response,False)
  await web.writefooters(response,chunked=False) #close
  try:
   del webserver_contr
  except:
   pass
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver controllers error: "+str(e))

@MicroWebSrv.route('/hardware',methods=['GET','POST'])
async def handle_hw(request,response):
 try:
  gc.collect()
  import webserver_hw
  web.writeheaders(response,chunked=False) #200 ok
  await webserver_hw.handle_hw(request,response,False)
  await web.writefooters(response,chunked=False) #close
  del webserver_hw
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver hw error: "+str(e))

@MicroWebSrv.route('/devices',methods=['GET','POST'])
async def handle_dev(request,response):
 try:
  if request.query is not None:
    responsearr = web.parse_qs(request.query)
  else:
    responsearr = []
  taskIndex = ("index" in responsearr and responsearr["index"] or '')
  taskIndexNotSet = (taskIndex == 0) or (taskIndex == '')
  web.writeheaders(response,chunked=False) #200 ok
  gc.collect()
  if taskIndexNotSet:
   from webserver_devlist import handle_devlist
   await handle_devlist(request,response,False)
  else:
   from webserver_dev import handle_device
   await handle_device(request,response,False)
  await web.writefooters(response,chunked=False) #close
  try:
   if taskIndexNotSet:
    del webserver_devlist
   else:
    del webserver_dev
  except:
   pass
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver dev error: "+str(e))

@MicroWebSrv.route('/rules',methods=['GET','POST'])
async def handle_rules(request,response):
 try:
  gc.collect()
  import webserver_rules
  web.writeheaders(response,chunked=False) #200 ok
  await webserver_rules.handle_rules(request,response,False)
  await web.writefooters(response,chunked=False) #close
  del webserver_rules
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver rules error: "+str(e))

@MicroWebSrv.route('/notifications',methods=['GET','POST'])
async def handle_notif(request,response):
 try:
  gc.collect()
  import webserver_notif
  web.writeheaders(response,chunked=False) #200 ok
  await webserver_notif.handle_notif(request,response,False)
  await web.writefooters(response,chunked=False) #close
  del webserver_notif
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver rules error: "+str(e))

@MicroWebSrv.route('/sysinfo')
async def handle_sysinfo(request, response):
 try:
  gc.collect()
  import webserver_sysinfo
  web.writeheaders(response,chunked=False) #200 ok
  await webserver_sysinfo.handle_sysinfo(request,response,False)
  await web.writefooters(response,chunked=False) #close
  del webserver_sysinfo
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver root error: "+str(e))

@MicroWebSrv.route('/blescanner')
async def handle_blescan(request, response):
 try:
  gc.collect()
  import webserver_blescan
  web.writeheaders(response,chunked=False) #200 ok
  await webserver_blescan.handle_blescan(request,response,False)
  await web.writefooters(response,chunked=False) #close
  del webserver_blescan
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver blescan error: "+str(e))

@MicroWebSrv.route('/i2cscanner')
async def handle_i2cscan(request, response):
 try:
  gc.collect()
  import webserver_i2cscan
  web.writeheaders(response,chunked=False) #200 ok
  await webserver_i2cscan.handle_i2cscan(request,response,False)
  await web.writefooters(response,chunked=False) #close
  del webserver_i2cscan
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver i2c scan error: "+str(e))

@MicroWebSrv.route('/wifiscanner')
async def handle_wifiscan(request, response):
 try:
  gc.collect()
  import webserver_wifiscan
  web.writeheaders(response,chunked=False) #200 ok
  await webserver_wifiscan.handle_wifiscan(request,response,False)
  await web.writefooters(response,chunked=False) #close
  del webserver_wifiscan
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver wifi scan error: "+str(e))

@MicroWebSrv.route('/sysvars')
async def handle_sysvars(request, response):
 try:
  gc.collect()
  import webserver_sysvars
  web.writeheaders(response,chunked=False) #200 ok
  await webserver_sysvars.handle_sysvars(request,response,False)
  await web.writefooters(response,chunked=False) #close
  del webserver_sysvars
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver sysvars error: "+str(e))

@MicroWebSrv.route('/log')
async def handle_log(request, response):
 try:
  gc.collect()
  import webserver_log
  web.writeheaders(response,chunked=False) #200 ok
  await webserver_log.handle_log(request,response,False)
  await web.writefooters(response,chunked=False) #close
  del webserver_log
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver log error: "+str(e))

@MicroWebSrv.route('/tools',methods=['GET','POST'])
async def handle_tools(request, response):
 try:
  gc.collect()
  import webserver_tools
  web.writeheaders(response,chunked=False) #200 ok
  await webserver_tools.handle_tools(request,response,False)
  await web.writefooters(response,chunked=False) #close
  del webserver_tools
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver tools error: "+str(e))

@MicroWebSrv.route('/rules',methods=['GET','POST'])
async def handle_rules(request, response):
 try:
  gc.collect()
  import webserver_rules
  web.writeheaders(response,chunked=False) #200 ok
  await webserver_rules.handle_rules(request,response,False)
  await web.writefooters(response,chunked=False) #close
  del webserver_rules
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver rules error: "+str(e))

@MicroWebSrv.route('/advanced',methods=['GET','POST'])
async def handle_adv(request, response):
 try:
  gc.collect()
  import webserver_adv
  web.writeheaders(response,chunked=False) #200 ok
  await webserver_adv.handle_adv(request,response,False)
  await web.writefooters(response,chunked=False) #close
  del webserver_adv
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver adv error: "+str(e))

@MicroWebSrv.route('/notifications',methods=['GET','POST'])
async def handle_adv(request, response):
 try:
  gc.collect()
  import webserver_notif
  web.writeheaders(response,chunked=False) #200 ok
  await webserver_notif.handle_notif(request,response,False)
  await web.writefooters(response,chunked=False) #close
  del webserver_notif
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver notif error: "+str(e))

@MicroWebSrv.route('/update',methods=['GET','POST'])
async def handle_ota(request, response):
 try:
  gc.collect()
  import webserver_ota
  web.writeheaders(response,chunked=False) #200 ok
  if request.method == "POST":
   await webserver_ota.handle_upload(request,response,False)
  else:
   await webserver_ota.handle_ota(request,response,False)
  await web.writefooters(response,chunked=False) #close
  del webserver_ota
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver ota error: "+str(e))

@MicroWebSrv.route('/dash',methods=['GET','POST'])
async def handle_dash(request, response):
 try:
  gc.collect()
  import webserver_dash
  web.writeheaders(response,chunked=False) #200 ok
  await webserver_dash.handle_dash(request,response,False)
  await web.writefooters(response,chunked=False) #close
  del webserver_dash
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver dash error: "+str(e))

@MicroWebSrv.route('/control',methods=['GET'])
async def handle_control(request, response):
 try:
  gc.collect()
  import webserver_command
  web.writeheaders(response,chunked=False) #200 ok
  await webserver_command.handle_command(request,response,False)
  await web.writefooters(response,chunked=False) #close
  del webserver_command
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver command error: "+str(e))

@MicroWebSrv.route('/csv',methods=['GET'])
async def handle_csv(request, response):
 try:
  gc.collect()
  import webserver_csv
  web.writeheaders(response,content="text/csv",chunked=False) #200 csv
  await webserver_csv.handle_csv(request,response,False)
  await web.writefooters(response,chunked=False) #close
  del webserver_csv
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver csv error: "+str(e))

@MicroWebSrv.route('/json',methods=['GET'])
async def handle_json(request, response):
 try:
  gc.collect()
  import webserver_json
  web.writeheaders(response,content="application/json",chunked=False) #200 json
  await webserver_json.handle_json(request,response,False)
  await web.writefooters(response,chunked=False) #close
  del webserver_json
  gc.collect()
 except Exception as e:
  misc.addLog(pglobals.LOG_LEVEL_ERROR, "Webserver json error: "+str(e))
