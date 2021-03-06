# you need to install imgproc from https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/robot/image_processing/
# програма по квадратику в центрі зображення з камери усереднює значення кольору і коли маємо заданий колір то 
# вмикаємо реле


from imgproc import * # img processing

from gpiozero import LED # RPI output
from time import sleep
import time


#
import math
#

ref_red = 45
ref_green = 45
ref_blue = 45
threshold = 60 #96

def timer():
    return time.time() #* 1000


def colorDetection(r, g, b):
    # subtract the pixel colour from the reference
    d_red = ref_red - red
    d_green = ref_green - green
    d_blue = ref_blue - blue

    #print "r:" + str(r) + " g:" + str(g) + " b:" + str(b)

    # length of the difference vector
    length = math.sqrt( (d_red * d_red) + (d_green * d_green) + (d_blue * d_blue) ) # distance between two dots into 3D space

    print length

    if length > threshold:
        return 0
    #         img_2[x, y] = 0, 0, 0
    else:
        return 1
    #         img_2[x, y] = 255, 255, 255





prevTimer = 0.0 # timer previous value
flagSole = True  
out = LED(17) # pinout

width = 320
heigh = 240

my_camera = Camera(width, heigh)
sensetivity = 10 #difference between r g b variables

#waitTime(5000) # wait for 5 seconds, so we can see the changes

my_image = my_camera.grabImage() # take a photo (I placed it because the line under needs some members from my_image)
    
my_view = Viewer(my_image.width, my_image.height, "Basic image processing") # GUI window

while True: # endless loop

    my_image = my_camera.grabImage() 

# red lines of target
    for x in range(0, my_image.width, 1):
        if x > (width/2 - 10) and x < (width/2 + 10):
            #print "0"
            pass
        #elif:
        else:
            my_image[x, heigh/2] = 255, 0, 0
            
        if x > (heigh/2 - 10) and x < (heigh/2 + 10): #x > 110 and x < 130
            #print "0"
            pass
        #elif:
        else:
            my_image[width/2, x] = 255, 0, 0
    
# sum of r g b incide square 20 * 20
    genR, genG, genB = my_image[0, 0]    #  my_image[x, y] return 3 int vars (rgb)
    
    for x in range(width/2-10, width/2+10 +1, 1): # 20
        for y in range(heigh/2-10, heigh/2+10 +1, 1):
            #print x, y
            # show red target square
            if (x==width/2-10 or y==heigh/2-10):
                my_image[x-1, y-1] = 255, 0, 0
            elif (x==width/2+10 or y==heigh/2+10):
                my_image[x+1, y+1] = 255, 0, 0
            
            if (x - y) == 40: # width 320 / 2 = 160 - heigh 240/2 = 120 = 40
                #print 'l'
                red, green, blue = my_image[x, y]
                #print "x = " + str(x) + " y = " + str(y) + '[' + str(red) + ' ' + str(green) + ' ' + str(blue) + ']'
                genR+=red
                genG+=green
                genB+=blue
                if x == width/2+10: # 170 if width = 320 (/2+10)
                # you should avoid of placing any drawings incide this square because it caused influence on measurements
                    genR/=20 # average red incide square
                    genG/=20
                    genB/=20
                    
                    # white color detector
                    average = (genR + genG + genB)/3 
                    #print average
                    if (colorDetection(genR, genG, genB)): #abs(average - genR) < sensetivity and abs(average - genG) < sensetivity and abs(average - genB) < sensetivity):
                        print "White color"
                        #print flagSole
                        out.off()
                        flagSole = False
                        
                        prevTimer = timer()
                        
                    else: 
                        print "r:" + str(genR) + " g:" + str(genG) + " b:" + str(genB)
                        
                        if(timer() - prevTimer > 1.0 and not flagSole):
                            flagSole = True
                            prevTimer = timer()
                            out.on() # signal to robot ON
                            #print "OFF"
                        elif(timer() - prevTimer > 2.0 and flagSole):
                            out.off()
                        else:
                            #out.on() # signal to robot OFF
                            #print "ON"
                            pass
                        #sleep(1)
                        
                
                
                #print genR # it isn't work here 
             
             #print genR
             #print "l" + str(genG)
             #print "l" + str(genB)
                      

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

