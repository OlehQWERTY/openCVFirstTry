from imgproc import *
my_camera = Camera(320, 240)
my_image = my_camera.grabImage()


# open a view setting the view to the size of the captured image
my_view = Viewer(my_image.width, my_image.height, "Basic image processing")

# display the image on the screen
my_view.displayImage(my_image)

# wait for 5 seconds, so we can see the changes
waitTime(5000)


# get the value of the pixel at x position 120 and y position 64 in the image
pixel = my_image[120, 64]
# pixel is now a tuple of the red, green and blue of the requested pixel

# An alternative method
red, green, blue = my_image[120, 64]
# red, green and blue now contain the intensity of the red, green and blue
# channels respectively

print "RED: "

print red