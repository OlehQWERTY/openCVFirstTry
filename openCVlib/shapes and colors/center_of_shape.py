# python center_of_shape.py --image 2d-basic-shapes-chart-for-children.png

import argparse
import imutils
import cv2


import numpy as np

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())

# load the image, convert it to grayscale, blur it slightly,
# and threshold it
image = cv2.imread(args["image"])




boundaries = [
	([40, 200, 200], [110, 255, 255])#, #mine yellow
	# ([86, 31, 4], [220, 88, 50]),
	# ([25, 146, 190], [62, 174, 250]),
	# ([103, 86, 65], [145, 133, 128])
]

for (lower, upper) in boundaries:
	# create NumPy arrays from the boundaries
	lower = np.array(lower, dtype = "uint8")
	upper = np.array(upper, dtype = "uint8")
 
	# find the colors within the specified boundaries and apply
	# the mask
	mask = cv2.inRange(image, lower, upper)
	output = cv2.bitwise_and(image, image, mask = mask)

	# cv2.imshow("images", np.hstack([image, output]))
	# cv2.waitKey(0)

# mask = cv2.inRange(image, [17, 15, 100], [50, 56, 200]) # mask = cv2.inRange(image, lower, upper)
# output = cv2.bitwise_and(image, image, mask = mask)
 
# show the images
# cv2.imshow("images", np.hstack([image, output]))



# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# gray = cv2.cvtColor(np.hstack([image, output]), cv2.COLOR_BGR2GRAY) # double image (original and prev)
gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

# cv2.imshow("Image", gray) # debug   # (255 - gray)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]

# cv2.imshow("Image", thresh) # debug

# find contours in the thresholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
# loop over the contours
for c in cnts:
	# compute the center of the contour
	M = cv2.moments(c)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])

	# draw the contour and center of the shape on the image
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
	cv2.putText(image, "center", (cX - 20, cY - 20),
	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

	# show the image
	cv2.imshow("Image", image)
	cv2.waitKey(0)
