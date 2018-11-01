import os
out = os.popen('python3 mod_find_obj.py ../2experiment/opencv_frame_2.png ../1experiment/frame_0-cropped_1.png').read()
#python3 mod_find_obj.py ../2experiment/opencv_frame_2.png ../1experiment/frame_0-cropped_1.png

#print(out)
#print(out.find('inliers/matched'))
if out.find('inliers/matched')!= -1:
    print("No sole!")
else:
    print("Sole detected!")
