import esp32

def read_cpu_temp():
 tc = 0
 try:
  tf = esp32.raw_temperature()
  tc = (tf-32.0)/1.8
 except:
  tc = 0
 return tc
