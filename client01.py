from check_timer import check_timer
import threading

def time_start():
    timer = threading.Timer(1, check_timer)
    timer.start()


