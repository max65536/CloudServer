from check_timer import check_timer
import threading


timer = threading.Timer(1, check_timer)
timer.start()


