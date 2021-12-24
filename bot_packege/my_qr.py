import PIL
import qrcode

def make_qr(arg):
    value_qr = str(arg)
    print('Запрошен: ' + value_qr)
    img = qrcode.make(value_qr)
    img.save('my_qr.png')
    return arg