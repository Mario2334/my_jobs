import logging
import sys
import threading

import easygui

from jobs_scrape import mine

logger = logging.getLogger(__name__)

def threaded(f, daemon=False):
    import Queue

    def wrapped_f(q, *args, **kwargs):
        '''this function calls the decorated function and puts the 
        result in a queue'''
        ret = f(*args, **kwargs)
        q.put(ret)

    def wrap(*args, **kwargs):
        '''this is the function returned from the decorator. It fires off
        wrapped_f in a new thread and returns the thread object with
        the result queue attached'''

        q = Queue.Queue()

        t = threading.Thread(target=wrapped_f, args=(q,) + args, kwargs=kwargs)
        logger.info('thread created')
        t.daemon = daemon
        t.start()
        t.result_queue = q
        return t

    return wrap


def run(data):
    choices = list()
    for i in data.keys():
        choices.append(i.encode('utf-8'))
    msg = 'New jobs %d' % len(data)
    title = 'New Jobs opportunities found'
    choice = easygui.choicebox(msg=msg, title=title, choices=choices)
    job_details = data[choice]
    job_desc = job_details[0][0]
    job_loc = job_details[1]
    no_of_bids = job_details[2][0]
    Payment = job_details[2][1]
    skills = job_details[0][1]
    easygui.textbox(msg=msg, title=title, text=
    '''
        {0}\nLocation : {1}\nDetails : {2}
        \n
        No of Bids : {3} \t Paymentx :{4} \n Skills : {5}
        '''.format(choice.encode('utf-8'), job_loc.encode('utf-8'), job_desc.encode('utf-8'),
                   str(no_of_bids).encode('utf-8'), Payment.encode('utf-8'), skills.encode('utf-8')))


def start():
    easygui.msgbox(
        'Welcome press one of the two keys to exit or else wait as job oppurtunies come flooding towards you from worknhire')
    sys.exit(1)


def get_data():
    import time
    logger.info('time has started')
    time.sleep(5 * 1 / 5)
    return mine().run()


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)

    return wrapped


if __name__ == '__main__':
    import stopwatch

    while 1:
        t = stopwatch.Timer()
        a = get_data()
        logger.info('length 1 ' + str(a[a.keys()[0]][0][0]))
        print 'time for mining' + str(t.elapsed)
        run(data=a)
        t.stop()
        print 'after whole' + str(t.elapsed)
        if easygui.ccbox():
            logger.info('accepted')
            continue
        else:
            logger.info('Cancelled')
            break
