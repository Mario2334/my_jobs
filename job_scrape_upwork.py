from bs4 import BeautifulSoup
from selenium import webdriver
import os
from datasets import mongoclient
from jobs_scrape_wnh import mine


class job_getter:
    def __init__(self):
#        path = '/home/hellrazer/PycharmProjects/my_jobs/chromedriver'
#        os.environ["webdriver.chrome.driver"] = path
        self.browser = webdriver.Chrome()
#        self.browser = webdriver.Firefox()
        self.base_url = 'https://www.upwork.com/o/jobs/browse/?from_recent_search=true&q=Python&sort=renew_time_int' \
                        '%2Bdesc '
        self.client = mongoclient('extracted jobs upwork')

    def render_page(self, url):
        self.browser.get(url)
        more_list = self.browser.find_elements_by_link_text('more')
        if len(more_list) > 0:
            for i in more_list:
                i.click()
        return BeautifulSoup(self.browser.page_source)

    def get_jobs(self):
        soup = self.render_page(self.base_url)
        jobs_list = soup.find('div', attrs={'id': 'jobs-list'})
        jobs_list = jobs_list.find_all('section', attrs={'class': 'job-tile'})
        for i in jobs_list:
            _id = i['data-key']
            title = mine.clean_string(i.find('h4', {'class': 'm-0'}).text)
            details = i.find('div', {'class': 'description break'}).find('span', attrs={
                'data-ng-bind-html': "htmlToTruncate"}).text
            price_type = i.find('strong', attrs={'class': 'js-type'}).text
            skill_level = i.find('span', attrs={'class': "js-contractor-tier"}).text.replace(' ', '').replace('($$)',
                                                                                                              '')
            try:
                budget = i.find('span', attrs={'itemprop': 'baseSalary'}).text
            except AttributeError:
                budget = mine.clean_string(i.find('span', attrs={'class': 'js-duration'}).text)
                pass
            print('_id: {} \n title : {} \n details : {} \n type: {} \n skill: {} \n budget : {} \n'.format(_id,
                                                                                                            title,
                                                                                                            details,
                                                                                                            price_type,
                                                                                                            skill_level,
                                                                                                            budget))
            pass


if __name__ == '__main__':
    job_getter().get_jobs()
