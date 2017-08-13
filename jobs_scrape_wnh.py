import datetime
import re

import requests
from bs4 import BeautifulSoup

from datasets import mongoclient


class mine:
    def __init__(self):
        self.base = 'http://worknhire.com'
        self.location = self.base + '/WorkProjects/jobs'
        self.keywords = open('C:\\Users\Hellrazer\PycharmProjects\my_jobs\Keywords').readlines()
        self.data_dict = dict()
        self.chosen_data_dict = dict()
        self.db = mongoclient('extracted jobs wnh')

    def parsing(self, location):
        data = requests.get(location)
        return BeautifulSoup(data.content, 'lxml')

    def run(self):
        data = self.parsing(self.location)
        # job_list = data.find_all('h2', attrs={'class': 'project-title'})
        self.interesting(data, self.keywords)
        print (len(self.chosen_data_dict.keys()))
        if len(self.chosen_data_dict) == 0:
            return True
        else:
            for i in self.chosen_data_dict.keys():
                print('found %s' % i)

            return self.chosen_data_dict

    def clean_string(self, data):
        return re.sub(pattern='\s*\n\s*', repl='', string=data)

    def data_posted(self, element_inst):
        date_posted = element_inst.find('span', attrs={'class': 'posted'}).text
        date_identify_index = ['hours', 'min']
        for i in date_identify_index:
            if i in date_posted:
                return str(datetime.datetime.today()).strip(r'[.]\d+')
            else:
                return date_posted

    def checker(self, page, keyword):
        curr_occ = 0
        for i in page:
            for z in keyword:
                z = z.strip('\n')
                if z in i:
                    curr_occ += 1
        return curr_occ

    def interesting(self, soup_page, keyword):  # checking jobs page for clues
        print('running interesting')
        job_listing = soup_page.find_all('div', {'class': 'jobdetails'})
        matcher_1 = re.compile("(.)+(?=[.]{3})")
        for i in job_listing:
            title = i.find('h2', {'class': 'project-title'}).a.text
            details = i.find('div', {'class': 'job-detail'}).find_all('div', {'class': 'desc'})
            if len(details) > 1:
                details = details[1].text
            else:
                details = details[0].text
            #            details = re.sub(matcher_1,'',details).replace('...','')
            location = i.find('h2', {'project-title'}).a['href']
            skills = i.find("div", {'class': 'ptopleft1'}).text
            date_posted = self.data_posted(i)
            a = self.checker((title, details, skills), keyword)
            data_dict = {'title': title, 'details': details, 'skills': skills, 'location': location,
                         'date posted': date_posted}
            if a > 0 and not self.db.check_if_data_present(data_dict):
                self.chosen_data_dict[title] = [[details, skills], 'http://www.worknhire.com/' + location]
                self.chosen_data_dict[title].append(self.get_values(self.base + location))
            self.db.insert_data(data_dict)

    def get_values(self, location):  # get accepted filter job data
        soup = self.parsing(str(location))
        try:
            no_bids = len(soup.find_all('div', {'class': 'job-bidder'}))
            time_frame = soup.find('div', {'id': 'info'})
            time_frame = time_frame.find('div', {'class': 'heading'}).span.text
        except:
            no_bids = 'Not Available'
            time_frame = 'Not Available'
        return (no_bids, time_frame)


if __name__ == '__main__':

    a = mine().run()
    if a is None:
        print('Nooooooo')
