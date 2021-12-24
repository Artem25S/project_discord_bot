from pyzbar import pyzbar
import cv2

def get_qr(arg):
    img = cv2.imread(arg)
    barcodes = pyzbar.decode(img)

    for barcode in barcodes:
        barcodeData = barcode.data.decode('utf-8')
        return  barcodeData
