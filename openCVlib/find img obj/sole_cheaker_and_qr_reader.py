# call pyLaunchCV.py -> python3 mod_find_obj.py ../2experiment/opencv_frame_2.png ../1experiment/frame_0-cropped_1.png where autoImg.png

# image from web camera and ../1experiment/frame_0-cropped_1.png - part of surface under sole

# detect sole that is located above prew prepared surface (picture that looks like chess mash)

import os
import cv2
import time


def nothing(x):
    pass

cam = cv2.VideoCapture(0)

# cv2.namedWindow("test")

img_counter = 0
out1 = os.popen('mkdir test_images 2> /dev/null').read() # save images for debugging wron guesture

# ret, frame = cam.read() #del
# cv2.imshow("test_cam", frame) #del
while True:
	for x in range(5):
		ret, frame = cam.read()
		if not ret:
			break

	start_time = time.time() #time counter

	frameToShow = frame.copy();
	# frame = cv2.resize(frame,(320,240)) # resize to lower resolution
# qr
	x1_1 = 120
	y1_1 = 70

	x1_2 = 260
	y1_2 = 170
# sole
	x2_1 = 60
	y2_1 = 110 # 220

	x2_2 = 640
	y2_2 = 320 # 430
	# cv2.putText(frameToShow, "OpenCV + Jurassic Park!!!", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
	# frameToShow = cv2.resize(frame,(640,480)) # resize to lower resolution
	cv2.rectangle(frameToShow, (x1_1, y1_1), (x1_2, y1_2), (0, 0, 255), 2)
	cv2.rectangle(frameToShow, (x2_1, y2_1), (x2_2, y2_2), (255, 0, 0), 2)


	cv2.namedWindow('test_cam') # create window with name (for Trackbar)
	cv2.createTrackbar('camResolution','test_cam',3,4,nothing) # trackbar
	resW = cv2.getTrackbarPos('camResolution','test_cam') # trackbar read position
	setCamW = pow(2, resW) * 80 # 160*120 320*240 640*480 1280*720
	setCamH = setCamW * 3/4

	cv2.putText(frameToShow, str(setCamW) + '*' + str(setCamH), (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
	
	# print(r * 160) 
	cv2.imshow("test_cam", frameToShow)
		# cv2.imshow("test_cam", frame)
		

	k = cv2.waitKey(1)
	if k%256 == 27:
		# ESC pressed
		print("Escape hit, closing...")
		break
	elif k%256 == 32:

		# SPACE pressed

		roi = frame[y2_1:y2_2, x2_1:x2_2] # roi = frame[y1:y2, x1:x2] 

		img_name = "autoImg.png" #img_name = "opencv_frame_{}.png".format(img_counter)
		cv2.imwrite(img_name, roi) #cv2.imwrite(img_name, frame)
		# print("{} written!".format(img_name))
		out = os.popen('python3 mod_find_obj.py autoImg.png cropped_texture_frames/texture_frame_cropped_1.png 2> /dev/null').read()
		print(out)
		if out.find('inliers/matched') != -1:
			print("No sole!")
		else:
			print("Sole detected!")
# ROI
		# roi1 = frame[x1_1:y1_1, x1_2:y1_2] # roi = frame[y1:y2, x1:x2] # error image data is empty
		zbarFrame = frame[y1_1:y1_2, x1_1:x1_2];
		img_name1 = "autoImgQR.png"
		cv2.imwrite(img_name1, zbarFrame)
		# cv2.imwrite(img_name1, roi1)

		# out1 = os.popen('convert ' + img_name + ' -crop 128x128+210+80 ' + img_name1).read()

		# out1 = os.popen('zbarimg ' + img_name1 + ' | grep "QR-Code:" | tr -dc \'0-9\'').read() # 2> /dev/null 
		out1 = os.popen('zbarimg ' + img_name1 + ' | grep "QR-Code:" | tr -dc \'0-9\' 2> /dev/null').read() # 2> /dev/null
		print(len(out1))
		if len(out1):
			print("Pos: ", out1)
		else:
			print("No QR code")

		# out1 = "no"

		elapsed_time = time.time() - start_time
		print("Time is: %f" % elapsed_time)


		# out2 = os.popen('date | tr " " _ | tr : ^ | tr -dc "\'0-9\'_^" | cut -c 2-18').read()
		out2 = os.popen('date +"%m-%d-%Y-%T" | tr : -').read()
		
			
		if out.find('inliers/matched') != -1:
			out3 = os.popen('cp autoImg.png ./test_images/' + out2[:-1] + '_pos_' + out1 + '_sole_' + 'On' + '.png').read() # [:-1] because \n # change it to normal view
		else:
			out3 = os.popen('cp autoImg.png ./test_images/' + out2[:-1] + '_pos_' + out1 + '_sole_' + 'OFF' + '.png').read() # [:-1] because \n


		# out3 = os.popen('ps ax | grep "sole_che*"').read()

		# print(out3)

		# words = out3.split(' ')
		# print(words[1]) #pid number

cam.release()

cv2.destroyAllWindows()