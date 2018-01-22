from threading import Timer,Lock
from jobs_scrape_wnh import mine
from intsla_scrapper import internshala

class Periodic(object):

    def __init__(self , interval ,  function , *args , **kwargs):
        self._lock = Lock()
        self._timer = None
        self.function = function
        self.interval = interval
        self.args = args
        self.kwargs = kwargs
        self.stopped = True
        if kwargs.pop('autostart' , True):
            self.start()

    def start(self , from_run = False):
        self._lock.acquire()
        if from_run or self.stopped:
            self.stopped = False
            self._timer = Timer(self.interval , self._run)
            self._timer.start()
            self._lock.release()

    def _run(self):
        self.start(from_run=True)
        self.function(*self.args , **self.kwargs)

    def stop(self):
        self._lock.acquire()
        self._stopped = True
        self._timer.cancel()
        self._lock.release()


if __name__ == '__main__':
        wnh = Periodic(60*5 , mine().run)
        internsl = Periodic(60*10 , internshala().run , True)