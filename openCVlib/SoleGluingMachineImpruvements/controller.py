#controller
import cv2
import barcode #barcode scaner
import findObj #findObject

cam = cv2.VideoCapture(0)

# while True:
# frame = cv2.imread("_2__2018_09:23:47_pos_no_sole_OFF.PNG", 0)

findObj.main()

for x in range(5):
	ret, frame = cam.read()
	if not ret:
		break

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
barcode.zbar(gray)

