#!/bin/bash

# exec 3>&1 4>&2
# trap 'exec 2>&4 1>&3' 0 1 2 3
# exec 1>log.out 2>&1
# Everything below will go to the file 'log.out':

# while :
# do
# echo "Press [CTRL+C] to stop.."
# sleep 1
cat /home/pi/strace/out.txt.* | grep 'write(1, \"QR*'
cat /home/pi/strace/out.txt.* | grep inliers/matched
rm /home/pi/strace/*.txt.*
# done

# strace -ff -e trace=write -e write=3 -p 2066 -o strace/out.txt

# cat strace/out.txt.2066 | grep "write(1, "

# cat strace/out.txt.2066 | grep "write*" >> strace/out.txt

