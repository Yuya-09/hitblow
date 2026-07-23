import time

start_time = None

def start():
    global start_time
    start_time = time.time()

def elapsed():
    if start_time is None:
        return 0
    return int(time.time() - start_time)