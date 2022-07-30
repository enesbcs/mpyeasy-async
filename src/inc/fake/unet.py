import settings
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
    _is_wlan = True
    _is_lan = True
    return _is_wlan, _is_lan

def lan_init(force=False):
    _lan_mode = 1
    return True

def lan_isconnected():
    return True

def wifi_sta_mode(ordn=1):
     wifi_sta = None
     _current_ssid = 0
     return False

def wifi_sta_isconnected():
    return True

def wifi_sta_disconnect(force=False):
    pass

def wifi_ap_mode():
    pass

def wifi_ap_stop(force=False):
    pass

def get_ip(nm="",clip=""):
      return '0.0.0.0'

def get_rssi():
    return -100

def get_ssid():
    return ''

def get_mac(nm=""):
    return ""

def setntp(ntpserver, timezone):
    return False

def get_net_const(cname):
    return 0
