try:
 import network
except:
 pass
import settings
try:
 import machine
except:
 pass
import inc.utime as utime

_active_mode = 0
_current_ssid  = 0
wifi_sta = None
lan_if = None
_lan_mode = 0
_is_wlan = False
_is_lan = False

def get_active_mode():
    global _active_mode
    return _active_mode

def get_wifi_sta():
    global wifi_sta
    return wifi_sta

def network_detect():
    global _is_wlan, _is_lan
    if _is_wlan==False and _is_lan==False:
       try:
        from network import WLAN
        _is_wlan = True
       except:
        _is_wlan = False
       try:
        from network import WIZNET5K
        _is_lan = True
       except:
        _is_lan = False
    return _is_wlan, _is_lan

def lan_init(force=False):
    global _lan_mode, lan_if
    if force:
       _lan_mode=0
    if _lan_mode==1:
      return True
    try:
     if lan_if is None:
      lan_if = network.WIZNET5K()
     if force:
        lan_if.active(False)
        utime.sleep_ms(1)
     if lan_if.active()==False:
      lan_if.active(True)
     if settings.Settings['LDHCP']==False:
          lan_if.ifconfig((settings.Settings['LIP'], settings.Settings['LMask'], settings.Settings['LGW'], settings.Settings['LDNS']))
     else:
          lan_if.ifconfig('dhcp')
     _lan_mode = 1
    except Exception as e:
     print("LAN connection error ",str(e))
     lan_if = None
     _lan_mode = 0

def lan_isconnected():
    global _lan_mode, lan_if
    if _lan_mode==1:
      try:
       if lan_if.isconnected():
        return True
      except:
        return False
    return False

def wifi_sta_mode(ordn=1):
    global _active_mode, _current_ssid, wifi_sta
    try:
     wifi_sta = network.WLAN(network.STA_IF)
    except:
     wifi_sta = None
     _current_ssid = 0
     return False
    _active_mode = (_active_mode | 1)
    forceconn = False
    if wifi_sta.isconnected():
      try:
         if settings.Settings['WDHCP']==False:
          wifi_sta.ifconfig((settings.Settings['WIP'], settings.Settings['WMask'], settings.Settings['WGW'], settings.Settings['WDNS']))
      except Exception as e:
         forceconn = True
    if not wifi_sta.isconnected() or forceconn:
        try:
         wifi_sta.active(True)
         if settings.Settings['WDHCP']==False:
          wifi_sta.ifconfig(config(settings.Settings['WIP'], settings.Settings['WMask'], settings.Settings['WGW'], settings.Settings['WDNS']))
        except Exception as e:
          pass
        _current_ssid = ordn
        try:
         if ordn==1 and settings.Settings['AP1SSID']:
          wifi_sta.connect(settings.Settings['AP1SSID'], settings.Settings['AP1KEY'])
         elif ordn==2 and settings.Settings['AP2SSID']:
          wifi_sta.connect(settings.Settings['AP2SSID'], settings.Settings['AP2KEY'])
        except:
         _current_ssid = 0

def wifi_sta_isconnected():
    global _active_mode, wifi_sta
    try:
     if (_active_mode & 1) == 1:
      wifi_sta = network.WLAN(network.STA_IF)
      if wifi_sta.isconnected():
        return True
    except:
     pass
    return False

def wifi_sta_disconnect(force=False):
    global _active_mode, _current_ssid, wifi_sta
    if ((_active_mode & 1) == 1) or force:
     try:
      wifi_sta = network.WLAN(network.STA_IF)
      wifi_sta.disconnect()
      wifi_sta.active(False)
     except:
      pass
     _current_ssid = 0
     if ((_active_mode & 1) == 1):
      _active_mode = _active_mode - 1

def wifi_ap_mode():
    global _active_mode
    if ((_active_mode & 2) == 2):
     return True
    try:
      wifi_ap = network.WLAN(network.AP_IF)
      wifi_ap.config(essid=settings.Settings["APSSID"],password=settings.Settings["APKEY"])
      print("Started SSID for config",settings.Settings["APSSID"])
      wifi_ap.active(True)
      _active_mode = (_active_mode | 2)
    except Exception as e:
      print(e)
    captiveok = False
    try:
     if settings.Settings["APCAPTIVE"]:
        wifi_ap.ifconfig( ('172.217.28.1','255.255.255.0','172.217.28.1','172.217.28.1') )
        try:
          from inc.tinydns.dns import Server
          dnsserver = Server(domains={ '*' : '172.217.28.1' })
          if dnsserver.sock is None:
           dnsserver.run()
          print("Captive DNS started at http://172.217.28.1")
          captiveok = True
        except Exception as e:
          print("Captive DNS failed ",e)
          captiveok = False
    except:
     pass
    if captiveok == False:
     wifi_ap.ifconfig( ('192.168.4.1','255.255.255.0','192.168.4.1','192.168.4.1') )
     print("AP started at http://192.168.4.1")

def wifi_ap_stop(force=False):
   global _active_mode
   if ((_active_mode & 2) == 2) or force:
    wifi_ap = network.WLAN(network.AP_IF)
    wifi_ap.active(False)
    if ((_active_mode & 2) == 2):
     _active_mode = _active_mode - 2

def get_ip(nm="",clip=""):
   global _active_mode, _lan_mode, lan_if
   wlan = None
   if (((_active_mode & 3) == 3) or (_lan_mode==1)) and (clip != ""):
    prob1 = 0
    try:
     wlan = network.WLAN(network.STA_IF)
     ipstr1 = wlan.ifconfig()[0]
     prob1 = ipcompare(ipstr1,clip)
    except:
     pass
    prob2 = 0
    try:
     wlan = network.WLAN(network.AP_IF)
     ipstr2 = wlan.ifconfig()[0]
     prob2 = ipcompare(ipstr2,clip)
    except:
     pass
    prob3 = 0
    try:
     if (_lan_mode==1):
      wlan = lan_if
      ipstr3 = wlan.ifconfig()[0]   
      prob3 = ipcompare(ipstr3,clip)
    except:
     pass
    if prob1>prob2 and prob1>prob3:
      return ipstr1
    elif prob2>prob1 and prob2>prob3:
      return ipstr2
    elif prob3>prob1 and prob3>prob2:
      return ipstr3
    
   if nm=="STA":
     try:
      wlan = network.WLAN(network.STA_IF)
     except:
      return '0.0.0.0'
   elif nm=="AP":
     try:
      if (_active_mode & 2) == 2:
       wlan = network.WLAN(network.AP_IF)
     except:
      return '0.0.0.0'         
   elif nm=="LAN":
      wlan = lan_if
   else:
    if (_lan_mode==1):
      wlan = lan_if
    elif (_active_mode & 1) == 1:
      wlan = network.WLAN(network.STA_IF)
    elif (_active_mode & 2) == 2:
      wlan = network.WLAN(network.AP_IF)
    else:
      return '0.0.0.0'
   try:
    ipstr = wlan.ifconfig()[0]
   except:
    ipstr = '0.0.0.0'
   return ipstr

def get_rssi():
    global _active_mode, wifi_sta
    if (_active_mode & 1) == 1:
      wifi_sta = network.WLAN(network.STA_IF)
      try:
       return wifi_sta.status('rssi') #rssi is not supported by cyw43?
      except:
       pass
    return -100

def get_ssid():
    global _active_mode
    result = ""
    try:
     if (_active_mode & 1) == 1:
       wlan = network.WLAN(network.STA_IF)
     elif (_active_mode & 2) == 2:
      wlan = network.WLAN(network.AP_IF)
     else:
       return ''
     result = wlan.config('essid')
    except:
     pass
    return result

def get_mac(nm=""):
   global _active_mode, _lan_mode, lan_if
   result = ""
   wlan = None
   try:
    if nm=="STA":
      wlan = network.WLAN(network.STA_IF)
    elif nm=="AP":
      wlan = network.WLAN(network.AP_IF)
    elif nm=="LAN":
      wlan = lan_if
    else:
     if _lan_mode==1:
      wlan = lan_if
     elif (_active_mode & 1) == 1:
      wlan = network.WLAN(network.STA_IF)
     elif (_active_mode & 2) == 2:
      wlan = network.WLAN(network.AP_IF)
     else:
      return ""
    a = wlan.config('mac')
    result = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(a[0],a[1],a[2],a[3],a[4],a[5])
   except:
     return ""
   return result

def setntp(ntpserver, timezone):
   res = False
   try:
    import ntptime
    ntptime.host = ntpserver
    t = ntptime.time()
    tm = utime.gmtime(t+(timezone*60))
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
    res = True
   except:
    res = False
   return res

def get_net_const(cname):
 return 0

def ipcompare(ip1,ip2):
    ipa = str(ip1).split(".")
    ipb = str(ip2).split(".")
    c = 0
    for i in range(0,len(ipa)):
        try:
         if ipa[i]==ipb[i]:
             c+=1
        except:
         pass
    return c
