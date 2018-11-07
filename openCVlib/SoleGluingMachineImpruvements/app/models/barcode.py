# sudo apt-get install libzbar0

# windows: pip install pyzbar

import cv2
# import time

from pyzbar import pyzbar

# t1 = time.time()

# frame = cv2.imread("_2__2018_09:23:47_pos_no_sole_OFF.PNG", 0)

def zbar(frame):
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	barcodes = pyzbar.decode(gray)

	for barcode in barcodes:
		(x, y, w, h) = barcode.rect
		# print(x, y, w, h)

		barcodeData = barcode.data.decode("utf-8")
		barcodeType = barcode.type

		# print the barcode type and data to the terminal
		# print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
		return [barcodeType, barcodeData, x, y, w, h]

# t2 = time.time() - t1
# print(t2)