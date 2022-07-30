import os

thermalzone = -1

def read_cpu_temp():
 global thermalzone
 res = 0
 if thermalzone == -1:
  thermalzone = 0
  for i in range(20):
   try:
    if os.path.exists("/sys/class/thermal/thermal_zone"+str(i)+"/type"):
     with open('/sys/class/thermal/thermal_zone'+str(i)+'/type') as fp:
      tstr = fp.readline()
     if (tstr.find("cpu")>=0) or (tstr.find("x86")>=0) or (tstr.find("bcm") >= 0):
       thermalzone = i
       break
   except Exception as e:
    print(e)
 elif thermalzone == -2:
  res = read_cpu_temp_sensor()
  return res
 try:
   with open('/sys/devices/virtual/thermal/thermal_zone'+str(thermalzone)+'/temp') as fp:
      res = fp.readline()
 except:
   res = 0
   thermalzone = -2
 therm2 = str2num2(res)
 if therm2 > 300:
  therm2 = str2num2(therm2 /1000) 
 return therm2

def read_cpu_temp_sensor():
    t = []
    try:
     output = os.popen("sensors | grep Core")
     for line in output:
      if ":" in line:
       try:
        pline = line.split(":")
        pline2 = pline[1].split("C")
        t.append(float(re.sub("[^\d\.]", "", pline2[0].strip())))
       except Exception as e:
        pass
    except:
     pass
    if len(t)<1:
     return 0
    else:
     return(sum(t)/len(t))

def str2num(data):
 try:
  data + ''
  return float(data.replace(',','.'))
 except TypeError:
  return data

def str2num2(data):
 try:
  return round(str2num(data),2)
 except:
  return data
