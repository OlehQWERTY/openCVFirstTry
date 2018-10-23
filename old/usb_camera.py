from imgproc import *
width = 320
heigh = 240
my_camera = Camera(width, heigh)

#waitTime(5000)

my_image = my_camera.grabImage()
    
my_view = Viewer(my_image.width, my_image.height, "Basic image processing")
while True:

    my_image = my_camera.grabImage()


    # open a view setting the view to the size of the captured image
    #my_view = Viewer(my_image.width, my_image.height, "Basic image processing")

    for x in range(0, my_image.width, 1):
        if x > (width/2 - 10) and x < (width/2 + 10):
            #print "0"
            pass
        #elif:
        else:
            my_image[x, heigh/2] = 255, 128, 0
            
        if x > (heigh/2 - 10) and x < (heigh/2 + 10): #x > 110 and x < 130
            #print "0"
            pass
        #elif:
        else:
            my_image[width/2, x] = 255, 128, 0
            
            
    for x in range(width/2-10, width/2+10, 1):
        for y in range(heigh/2-10, heigh/2+10, 1):
            if x == y:
                print 'l'
                red, green, blue = my_image[x, y]
                print "x = " + str(x) + " y = " + str(y) + '[' + str(red) + ' ' + str(green) + ' ' + str(blue) + ']'
        
        

    # display the image on the screen
    my_view.displayImage(my_image)



    # wait for 5 seconds, so we can see the changes
    #waitTime(5000)


    # get the value of the pixel at x position 120 and y position 64 in the image
    #pixel = my_image[122, 64]
    # pixel is now a tuple of the red, green and blue of the requested pixel
    
    #print pixel

    # An alternative method
    #red, green, blue = my_image[120, 64]
    # red, green and blue now contain the intensity of the red, green and blue
    # channels respectively

    #print "RED: "

    #print red

