import re

import requests
from bs4 import BeautifulSoup


class mine:
    def __init__(self):
        self.base = 'http://worknhire.com'
        self.location = self.base + '/WorkProjects/jobs'
        self.keywords = open('Keywords').readlines()
        self.data_dict = dict()

    def parseing(self, location):
        data = requests.get(location)
        return BeautifulSoup(data.content, 'lxml')

    def run(self):
        data = self.parseing(self.location)
        # job_list = data.find_all('h2', attrs={'class': 'project-title'})
        self.interesting(data, self.keywords)
        if self.data_dict.keys() == 0:
            return True
        else:
            for i in self.data_dict.keys():
                print 'found %s' % i
            return self.data_dict

    def clean_string(self, data):
        return re.sub(pattern='\s*\n\s*', repl='', string=data)

    def checker(self, page, keyword):
        curr_occ = 0
        for i in page:
            for z in keyword:
                z = z.strip('\n')
                if z in i:
                    curr_occ += 1
        return curr_occ

    def interesting(self, soup_page, keyword):  # checking jobs page for clues
        print 'running interesting'
        job_listing = soup_page.find_all('div', {'class': 'jobdetails'})
        for i in job_listing:
            title = i.find('h2', {'class': 'project-title'}).a.text
            details = i.find('div', {'class': 'job-detail'}).text
            location = i.find('h2', {'project-title'}).a['href']
            skills = i.find("div", {'class': 'ptopleft1'}).text
            a = self.checker((title, details, skills), keyword)
            if a > 0:
                self.data_dict[title] = [[details, skills], location]
                self.data_dict[title].append(self.get_values(self.base + location))

    def get_values(self, location):  # get accepted filter job data
        soup = self.parseing(str(location))
        no_bids = len(soup.find_all('div', {'class': 'job-bidder'}))
        time_frame = soup.find('div', {'id': 'info'})
        time_frame = time_frame.find('div', {'class': 'heading'}).span.text
        return (no_bids, time_frame)


if __name__ == '__main__':
    a = mine().run()
    if a is None:
        print 'Nooooooo'
