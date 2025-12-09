import qrcode
from io import BytesIO
from flask import send_file

def get_QR(url):
    qr = qrcode.make(url)
    buf = BytesIO()
    qr.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png', as_attachment=False)


