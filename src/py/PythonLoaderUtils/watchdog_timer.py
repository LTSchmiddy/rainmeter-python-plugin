# NGL, I copy/pasted this entire file from a stackoverflow thread: https://stackoverflow.com/a/34115590
# The other, higher ranked methods weren't working (not to mention asyncio wouldn't import).
# Honestly, I'm not entirely sure why the 'threading' module works embedded, considering Python's 
# GIL and the thread handling I had to implement on the C++ side. Perhaps since it all takes 
# place inside the same C++ PyEval_RestoreThread/PyEval_SaveThread set?

from threading import Event, Lock, Thread
from time import monotonic

class WatchdogTimer(Thread):
    """
    Run *callback* in *timeout* seconds unless the timer is restarted.
    Used by subinterp to prevent permanent hanging.
    """

    def __init__(self, timeout, callback, *args, timer=monotonic, **kwargs):
        super().__init__(**kwargs)
        self.timeout = timeout
        self.callback = callback
        self.args = args
        self.timer = timer
        self.cancelled = Event()
        self.blocked = Lock()

    def run(self):
        self.restart() # don't start timer until `.start()` is called
        # wait until timeout happens or the timer is canceled
        while not self.cancelled.wait(self.deadline - self.timer()):
            # don't test the timeout while something else holds the lock
            # allow the timer to be restarted while blocked
            with self.blocked:
                if self.deadline <= self.timer() and not self.cancelled.is_set():
                    return self.callback(*self.args)  # on timeout

    def restart(self):
        """Restart the watchdog timer."""
        # print("""Restart the watchdog timer.""")
        self.deadline = self.timer() + self.timeout

    def cancel(self):
        self.cancelled.set()