#MAWF = Minimal Async Web Framework
try:
 import uasyncio as asyncio
except:
 import asyncio
from binascii import b2a_base64
import struct
import os
import gc

def redirect(stream,location):
    if stream:
     try:
      stream.write(b'HTTP/1.1 301 Moved Permanently\r\nLocation: '+ bytes(location,'utf-8') +b'\r\n\r\n')
      stream.close()
     except:
      pass

def writeheaders(stream, code=200,content="text/html",chunked=False):
    if code==200:
         stream.write(b'HTTP/1.1 200 OK\r\n')
    else:
         stream.write(b'HTTP/1.1 404 Not Found\r\n\r\nNot Found')
    stream.write(b'Content-Type: '+ bytes(content,'utf-8') + b'; charset=utf-8\r\n')
    if chunked:
         stream.write(b'Transfer-Encoding: chunked\r\n')
         stream.write(b'Keep-Alive: timeout=5, max=100\r\n')
    stream.write(b'\r\n')

async def send_file(stream, filename, content_type=None, max_age=2592000, buf_size=512):
        try:
            # Get file size
            stat = os.stat(filename)
            slen = stat[6]
            res = b"200 OK"
        except OSError as e:
            slen = -1
            res = b"404 Not found"
        try:
            stream.write(b'HTTP/1.1 '+ res + b'\r\n')
            if slen == -1:
             return -1
            if content_type:
             stream.write(b'Content-Type: '+ bytes(content_type,'utf-8') + b'\r\n')
            stream.write(b'Content-Length: '+ bytes(str(slen),'utf-8') + b'\r\n')
            stream.write(b'Cache-Control: max-age='+ bytes(str(max_age),'utf-8') + b',public\r\n\r\n')
            gc.collect()
            with open(filename,'rb') as f:
                buf = bytearray(min(slen, buf_size))
                while True:
                    size = f.readinto(buf)
                    if size == 0:
                        break
                    stream.write(buf)
                    await stream.drain()
        except Exception as e:
            print(e) # debug


def writebuffered(stream, bdystr,chunked=False,Force=False):
    if (len(bdystr)>128) or (Force):
     if chunked==False:
      stream.write(bytes(bdystr,'utf-8'))
      return True
     else:
      bstr = bytes(bdystr,'utf-8')
      bsize = len(bstr)
      stream.write( bytes(str(bsize),'utf-8')+ b'\r\n' + bstr + b'\r\n')
      return True
    return False

async def awrite(stream, bdystr, chunked=False, Force=False):
      res = writebuffered(stream, bdystr, chunked, Force)
      if res:
       await stream.drain()
      return res

async def writefooters(stream, chunked=False):
   try:
    if chunked:
        stream.write(b'0\r\n\r\n')
    await stream.drain()
    stream.close()
   except:
    pass

def unquote_plus(s):
    out = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        i += 1
        if c == '+':
            out.append(' ')
        elif c == '%':
            out.append(chr(int(s[i:i + 2], 16)))
            i += 2
        else:
            out.append(c)
    return ''.join(out)

def parse_qs(s):
    if s is None or len(s)<1:
     return []
    out = {}
    for x in s.split('&'):
        kv = x.split('=', 1)
        key = unquote_plus(kv[0])
        kv[0] = key
        if len(kv) == 1:
            val = True
            kv.append(val)
        else:
            val = unquote_plus(kv[1])
            kv[1] = val
        tmp = out.get(key, None)
        if tmp is None:
            out[key] = val
        else:
            if isinstance(tmp, list):
                tmp.append(val)
            else:
                out[key] = [tmp, val]
    return out

async def _parse_request(r, w):
    line = await r.readline()
    if not line:
        raise ValueError
    parts = line.decode().split()
    if len(parts) < 3:
        raise ValueError
    r.method = parts[0]
    r.path = parts[1]
    parts = r.path.split('?', 1)
    if len(parts) < 2:
        r.query = None
    else:
        r.path = parts[0]
        r.query = parts[1]
    r.headers = await _parse_headers(r)
    #print(r.path,r.headers,r.query)#debug
    if r.method == "POST":
       if ('content-type' not in r.headers) or ('content-length' not in r.headers):
        r.query = None
       else:
        try:
         size = int(r.headers['content-length'])
         data = await r.readexactly(size)
         r.query = data.decode("utf-8")  # application/x-www-form-urlencoded
        except:
         pass

async def _parse_headers(r):
    headers = {}
    while True:
        line = await r.readline()
        if not line:
            break
        line = line.decode()
        if line == '\r\n':
            break
        key, value = line.split(':', 1)
        headers[key.lower()] = value.strip()
    return headers

class App:

    def __init__(self, host='0.0.0.0', port=80):
        self.host = host
        self.port = port
        self.handlers = []

    def route(self, path, methods=['GET']):
        def wrapper(handler):
            self.handlers.append((path, methods, handler))
            return handler
        return wrapper

    async def _dispatch(self, r, w):
        try:
            await _parse_request(r, w)
        except:
            w.close()
            await w.wait_closed()
            return
        for path, methods, handler in self.handlers:
            if r.path != path:
                continue
            if r.method not in methods:
                continue
            await handler(r, w)
            try:
             await w.wait_closed()
            except Exception as e:
             print(e)
            return
        try:
         await w.awrite(b'HTTP/1.1 404 Not Found\r\n\r\nNot Found')
        except:
         w.write(b'HTTP/1.1 404 Not Found\r\n\r\nNot Found')
         await w.drain()
        w.close()
        await w.wait_closed()

    async def serve(self, host='', port=0):
        if host != '':
         self.host = host
        if port > 0:
         self.port = port
        await asyncio.start_server(self._dispatch, self.host, self.port)
