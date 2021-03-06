# call pyLaunchCV.py -> python3 mod_find_obj.py ../2experiment/opencv_frame_2.png ../1experiment/frame_0-cropped_1.png where autoImg.png

# image from web camera and ../1experiment/frame_0-cropped_1.png - part of surface under sole



# detect sole that is located above prew prepared surface (picture that looks like chess mash)



import os

import cv2



cam = cv2.VideoCapture(0)



# cv2.namedWindow("test")



img_counter = 0

out1 = os.popen('mkdir test_imgages').read()



while True:

	for x in range(5):

		ret, frame = cam.read()

		cv2.imshow("test", frame)

		if not ret:

			break



	k = cv2.waitKey(1)
	if k%256 == 27:
		# ESC pressed
		print("Escape hit, closing...")
		break
	elif k%256 == 32:

		

		# SPACE pressed

		img_name = "autoImg.png" #img_name = "opencv_frame_{}.png".format(img_counter)

		cv2.imwrite(img_name, frame)

		# print("{} written!".format(img_name))
 


		out = os.popen('python3 mod_find_obj.py autoImg.png frame_0-cropped_0.png').read()
		print(out)

		if out.find('inliers/matched') != -1:

			print("No sole!")
		else:

			print("Sole detected!")


		out1 = os.popen('zbarimg autoImg.png 2> /dev/null | grep "QR-Code:" | tr -dc \'0-9\'').read()
		#print(len(out1))
		if len(out1):

			print("Pos: ", out1)
		else:

			print("No QR code")

		out2 = os.popen('date | tr " " _ | tr -dc "\'0-9\'_:" | cut -c 2-18').read()
			
		if out.find('inliers/matched') != -1:
			out2 = os.popen('cp autoImg.png ./test_imgages/' + out2[:-1] + '_pos_' + out1 + '_sole_' + 'On' + '.png').read() # [:-1] because \n # change it to normal view
		else:
			out2 = os.popen('cp autoImg.png ./test_imgages/' + out2[:-1] + '_pos_' + out1 + '_sole_' + 'OFF' + '.png').read() # [:-1] because \n



cam.release()

cv2.destroyAllWindows()
