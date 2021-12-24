import PIL
import qrcode
# Метотод создания картинок c qr кодом для дальнейшего отправления в канал сервера
# print для контроля состояния преобразования
def make_qr(arg):
    value_qr = str(arg)
    print('Запрошен: ' + value_qr)
    img = qrcode.make(value_qr)
    img.save('my_qr.png')
    return arg