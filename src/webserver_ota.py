import webserver_global as ws
import pglobals
from web import awrite
try:
 import inc.esp32.lib_part as PartMgr
except Exception as e:
 print("ESP32 OTA",e)

async def handle_upload(request,response,chunk):
 ws.navMenuIndex=7
 ws.TXBuffer = ""

 try:
     import inc.lib_blehelper as BLEHelper
     _blestatus = BLEHelper.BLEStatus
 except:
     _blestatus = None
 if _blestatus is not None:
  try:
   if _blestatus.isscaninprogress(): #ble scan interferes ota
    _blestatus.requeststopscan(1)
    import time
    time.sleep(1)
    if _blestatus.isscaninprogress():
     _blestatus.forcestopscan()
  except:
   pass

 ws.sendHeadandTail("TmplStd",ws._HEAD)
 ws.TXBuffer += '<label for="file">File progress:</label><progress id="file" max="100" value="0"><span>0</span>%</progress>'
 if await awrite(response,ws.TXBuffer,chunked=chunk):
  ws.TXBuffer = ""

 buf = bytearray(4096)
 buf2 = bytearray(4096)

 try:
  pm = PartMgr.OTA()
  pm.initota()
  otaok = pm.success
 except:
  pm = None
  otaok = False

 if otaok==False:
  secok = False
  ws.TXBuffer += "<p>OTA init failed!"
 try:
  SEC_SIZE = pm.SEC_SIZE
 except:
  SEC_SIZE = 4096

 percent = 0
 secok = True
 hok = False
 lpage = False
 rsize = SEC_SIZE
 block = -1
 try:
  fs = int(request.headers['content-length'])
 except:
  fs = -1
 if fs is None or fs<=0:
  secok = False
  ws.TXBuffer += "<p>Browser did not sent upload size! Canceling upload."
 gptr = 0
 fptr = 0
 prevperc = 0
 imageok = True
 while secok:
  if gptr+rsize>fs:
   rsize=fs-gptr
   lpage = True
  if rsize<1:
   rsize = None
  try:
   buf = await request.readexactly(rsize) #read header await??
  except:
   secok = False
  if len(buf)<1:
   secok = False
  if secok:
   gptr += len(buf)
   if lpage:  #last page
    hend = buf.find(b'\r\n--')  # search header
    if hend:
     buf = buf[:hend]
     rsize = None
     percent = 100
   if hok==False: #first page
    hend = buf.find(b'\r\n\r\n')  # search header
    if hend:
     buf2 = buf[(hend+4):]
     hok = True
     rsize = SEC_SIZE-len(buf2)
    else:
     rsize = SEC_SIZE
   else: # file content
     rsize = SEC_SIZE
     if len(buf2)>0: #1st sector
      buf = buf2+buf
      buf2 = bytearray()
     fptr += len(buf)
     block += 1
     if percent < 100:
      percent = int(gptr*100/fs)
     try:
      if imageok:
       if block>=15:
        if block==15:
          if int(buf[0]) != 233:
           imageok = False
          print("start block",block,block-15,buf[0])#debug
        if len(buf)<SEC_SIZE:
         buf2 = bytearray(SEC_SIZE-len(buf))
         buf = buf+buf2
        pm.writedata(block-15,buf)
     except:
      imageok = False
     if prevperc!=percent:
      print("---->",percent,gptr,fptr,len(buf),block) # debug
      ws.TXBuffer += '<script type="text/javascript">var i = '
      ws.TXBuffer += str(percent)
      ws.TXBuffer += ';var progressBar = document.getElementById("ffile");progressBar.value = i;progressBar.getElementsByTagName("span")[0].textContent = i;</script>'
      if await awrite(response,ws.TXBuffer,chunked=chunk):
       ws.TXBuffer = ""
      prevperc=percent

 try:
  if pm.success==False or imageok==False:
   percent=0
 except:
  percent = 0
 if percent == 100:
   try:
    pm.endota()
   except:
    pass
   ws.TXBuffer += "<p>Upload completed! "
   ws.TXBuffer += " <a class='button link wide' href='/?cmd=reboot'>Reboot</a>"
 else:
   ws.TXBuffer += "<p>Upload failed!"
 ws.sendHeadandTail("TmplStd",ws._TAIL)
 await awrite(response,ws.TXBuffer,chunked=chunk,Force=True)
 ws.TXBuffer = ""

async def handle_ota(request,response,chunk):
 ws.navMenuIndex=7
 ws.TXBuffer = ""
 ws.sendHeadandTail("TmplStd",ws._HEAD)
 try:
  pm = PartMgr.partmgr()
  op = pm.isotasupported()
  pi = op.info()[3]
 except:
  pm = None
  op = False
  pi = 0
 oi = ""
 if op==False:
  oi = "NOT "
 ws.TXBuffer += "<p>OTA {0}SUPPORTED! Free space: {1} bytes".format(oi,pi)
 ws.TXBuffer += "<p><form enctype='multipart/form-data' method='post'><p>Upload file:<br><input type='file' name='firmware.bin' id='ffile'></p><div><input class='button link' type='submit' value='Upload'></div></form>"

 ws.sendHeadandTail("TmplStd",ws._TAIL)
 await awrite(response,ws.TXBuffer,chunked=chunk,Force=True)
 ws.TXBuffer = ""
