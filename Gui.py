import logging

import easygui


class GUI:
    def __init__(self, data):
        self.choices = []
        self.data_dict = data
        self.choices = list()
        self.logger = logging.getLogger(__name__)

    def run(self):
        while 1:
            for i in self.data_dict.keys():
                self.choices.append(i)

            msg = 'New jobs %d' % len(self.data_dict)
            title = 'New Jobs opportunities found'
            self.logger.info('applcation opened')
            choice = easygui.choicebox(msg=msg, title=title, choices=self.choices)
            self.logger.info('choice selected')
            job_details = self.data_dict[choice]
            job_desc = job_details[0][0]
            job_loc = job_details[1]
            no_of_bids = job_details[2]
            time_taken = job_details[3]
            skills = job_details[0][1]
            easygui.textbox(msg=msg, title=title, text=
            '''
            {0}\n<a>Location : {1}</a>\nDetails : {2}
            \n
            No of Bids : {3} \t Time required :{4} \n Skills : {5}
            '''.format(choice, 'http://www.worknhire.com/' + job_loc, job_desc, no_of_bids, time_taken, skills))
            break
