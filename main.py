import atexit
from cancellation import cancellation
from loop import loop

def on_exit_requested():
    cancellation.request_cancellation()

if __name__ == '__main__':
    atexit.register(on_exit_requested)
    loop()

