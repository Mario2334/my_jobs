from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from sortedcontainers import SortedDict
from utils.datasets import mongoclient
from scrapers import jobs_scrape_wnh
import os

class job_getter:
    def __init__(self):
        cap = DesiredCapabilities().FIREFOX
#         self.browser = webdriver.Chrome(executable_path="/Users/sanketmokashi/PycharmProjects/my_jobs/chromedriver")
        self.browser = webdriver.Firefox(capabilities=cap,executable_path="/Users/sanketmokashi/PycharmProjects/my_jobs/geckodriver")
        self.base_url = 'https://www.upwork.com/o/jobs/browse/?q=python&sort=recency'
        self.client = mongoclient('extracted jobs upwork')

    def render_page(self, url):
        import time
        self.browser.get(url)
        more_list = self.browser.find_elements_by_link_text('more')
        if len(more_list) > 0:
            for i in more_list:
                i.click()
        time.sleep(5)
        soup = BeautifulSoup(self.browser.page_source)
        self.browser.close()
        return soup

    def get_jobs(self):
        soup = self.render_page(self.base_url)
        # get jobs list

        jobs_list = soup.find_all("section", attrs={"class":"air-card air-card-hover job-tile-responsive ng-scope"})
        for job in jobs_list:
            title = job.find("a", attrs={"class": "job-title-link"})
            link = title["href"]
            title = title.find("span").text
            details = job.find("span", attrs={"class": "js-description-text"}).text

            try:
                budget = job.find("strong", attrs={"class": "js-workload"}).text
                price_type = "Hourly"
            except AttributeError :
                budget = job.find("strong", attrs={"class": "js-budget"}).text
                price_type = "Fixed"

            skill_level = job.find("strong",attrs = {"class" : "js-contractor-tier"}).text

            print('_id: {} \n title : {} \n details : {} \n type: {} \n skill: {} \n budget : {} \n'.format(link,
                                                                                                            title,
                                                                                                            details,
                                                                                                            price_type,
                                                                                                            skill_level,
                                                                                                            budget))
            self.client.insert_data(
                {
                    "title":link,
                    "details":details,
                    "price_type" : price_type,
                    "skill_level":skill_level,
                    "budget":budget,
                }
            )
        # topics, dets = self.split_data(jobs_list)

    @staticmethod
    def split_data(data):
        topics = list()
        details = list()
        for row in data:
            row = SortedDict(row)
            if data.index(row) == 0:
                topics = [i for i in row]
            details.append([row[data] for data in topics])
        return topics, details


if __name__ == '__main__':
    job_getter().get_jobs()
