import imgproc
from imgproc import *

# import maths module for the square root function
import math


width = 80
heigh = 60
# open a webcam to take pictures
camera = Camera(80, 60)

# Open a viewer window to display images
viewer = Viewer(width*4, heigh*4, "Colour Key")

# take a picture from the camera
img = camera.grabImage()

# display the image in the viewer
viewer.displayImage(img)


# constant variables used in the algorithm
ref_red = 192
ref_green = 80
ref_blue = 80
threshold = 96 #96


# take a picture from the camera
img = camera.grabImage()

#copy

img_2 = img



# iterate over each pixel in the image
while True:
    for threshold in range(120, 180, 10):
        img_2 = camera.grabImage()
        print threshold
        for x in range(0, img.width):
                for y in range(0, img.height):
                        red, green, blue = img_2[x, y]

                        # subtract the pixel colour from the reference
                        d_red = ref_red - red
                        d_green = ref_green - green
                        d_blue = ref_blue - blue

                        # length of the difference vector
                        length = math.sqrt( (d_red * d_red) + (d_green * d_green) + (d_blue * d_blue) )

                        if length > threshold:
                                img_2[x, y] = 0, 0, 0
                        else:
                                img_2[x, y] = 255, 255, 255
                                
                        


        # display the image again
        viewer.displayImage(img_2)

        # delay for 5000 milliseconds to give us time to see the changes, then exit
        #waitTime(1000)


    # end of the script
