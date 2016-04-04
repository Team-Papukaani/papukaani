import base64
import zlib

def compressedBase64ToString(b64s):
    byts_c = base64.b64decode(b64s)
    byts = zlib.decompress(byts_c)
    s = byts.decode('utf-8')
    return s

def stringToCompressedBase64(s):
    byts = s.encode('utf-8')
    byts_c = zlib.compress(byts)
    b64s = base64.b64encode(byts_c).decode('ascii')
    return b64s
