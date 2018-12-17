#!/usr/bin/bash
kill -9 controller.py # kill pid
python3 controller.py # start

# in py script 
# os.execl('restart.sh', '') 
# when I can't connect to web camera