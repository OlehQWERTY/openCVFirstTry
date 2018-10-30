#sudo apt-get install zbar-tools

import sys
import os

def start_cam():
    while True:
        #Initializes an instance of Zbar to the commandline to detect barcode data-strings.
        p=os.popen('/usr/bin/zbarcam --prescale=300x200','r')
        #Barcode variable read by Python from the commandline.
        print("Please Scan a QRcode to begin...")
        barcode = p.readline()
        barcodedata = str(barcode)[8:]

        if barcodedata:
            print("{0}".format(barcodedata))
            #Kills the webcam window by executing the bash file 
            os.system("/share/BarCode/kill.sh")

start_cam()