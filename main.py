import logging
import os
import sys
import threading
import time

import easygui

from jobs_scrape_wnh import mine

logger = logging


def getLogger():
    if not os.path.exists("log"):
        os.makedirs("log")

    file_name = 'logfile'

    logging.basicConfig(filename=file_name,
                        filemode="a+",
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


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
    if choice is None:
        return 0
    job_details = data[choice]
    job_desc = job_details[0][0]
    job_loc = job_details[1]
    no_of_bids = job_details[2][0]
    payment = job_details[2][1]
    skills = job_details[0][1]
    easygui.textbox(msg=msg, title=title, text=
    '''
        {0}\nLocation : {1}\nDetails : {2}
        \n
        No of Bids : {3} \t Payment :{4} \n Skills : {5}
        '''.format(choice.encode('utf-8'), job_loc.encode('utf-8'), job_desc.encode('utf-8'),
                   str(no_of_bids).encode('utf-8'), payment.encode('utf-8'), skills.encode('utf-8')))
    return 1


def start():
    easygui.msgbox(
        'Welcome press one of the two keys to exit or else wait as job oppurtunies come flooding towards you from worknhire')
    sys.exit(1)


def get_data():
    return mine().run()


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)

    return wrapped


def gui_inst(a):
    v = run(data=a)
    if v == 0:
        return True
    # t.stop()
    if easygui.ccbox():
        logger.info('accepted')
        return True
    else:
        logger.info('Cancelled')
        return False


if __name__ == '__main__':
    import re

    getLogger()

    while 1:
        a = get_data()
        if a == True:
            print("No interested data found")
            logger.info('No interested data found')
        else:
            print(type(a))
            print(len(a))
            a = gui_inst(a)
            if not a:
                logger.info('System exiting with status 1')
                print('system exiting in a minute')
                time.sleep(60)
                sys.exit(1)
        print('sleeping at %s' % re.sub(pattern='[.]\d+', string=time.strftime("%a, %d %b %Y %X +0000", time.gmtime()),
                                        repl=''))
        time.sleep(60 * 10)
