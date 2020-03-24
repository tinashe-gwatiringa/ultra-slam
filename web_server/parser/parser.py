import json
import os
import time

def parse(path, interval=2):

    if not os.path.exists(path):
        print('Path does not exist:', path)
        exit(1)
    else:
        last_modified = 0
        while True:
            if last_modified != os.path.getmtime(path):
                print('file modified:', path)
                last_modified = os.path.getmtime(path)
            else:
                time.sleep(interval)