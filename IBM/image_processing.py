import cv2
import base64
import cgi
import io
import numpy as np

# Credit to Pelle Jakovits
# https://github.com/pjakovits/FaaSfunc/blob/master/thumbnail_IBM_Functions/function.py

def main(param):
    png = param["__ow_body"]
    bindata = base64.b64decode(png)
    fp2 = io.BytesIO(bindata)
    form = cgi.FieldStorage(fp=fp2, environ={'REQUEST_METHOD': 'POST',
                                             'CONTENT_LENGTH': len(bindata),
                                             'CONTENT_TYPE': param["__ow_headers"]["content-type"]})
    dat = form["pic"]
    img_bytes = dat.file.read()
    np_arr = np.frombuffer(img_bytes, dtype='uint8')
    img_np = cv2.imdecode(np_arr, cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    retval, buffer = cv2.imencode('.jpg', gray)
    out = base64.b64encode(buffer)
    return {
        "isBase64Encoded": True,
        "statusCode": 200,
        "headers": {"content-type": "image/jpeg"},
        "body": out
    }

