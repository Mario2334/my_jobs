import csv
import datetime
import time

from selenium import webdriver

from datasets import mongoclient
from job_scrape_upwork import job_getter
from mail import mailer


class internshala():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.file = open('intern_info.csv', 'w')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['Date Posted', 'Title', 'Company', 'Locations', 'Stipend', 'Start Date', 'Duration'])
        self.url = 'https://internshala.com/internships/python%2Fdjango-internship'

    def run(self):
        now = datetime.datetime.now()
        if now.hour < 8 or now.hour > 22:
            return None
        if now.weekday() > 6:
            return None
        self.driver.get('https://internshala.com/internships/python%2Fdjango-internship')
        self.conn = mongoclient('internshala')
        data = self.get_posts(self.driver)
        filtered_data = list()
        self.driver.close()
        # if is_csv:
        #     for post in data:
        #         self.writer.writerow(post)
        # else:
        #     return data
        for interns in data:
            if not self.conn.check_id(interns['_id']):
                self.conn.insert_data(interns, True)
                filtered_data.append(interns)
        topics, details = job_getter.split_data(filtered_data)
        mailer('internship of internshala').send_html_email(topics=topics, details=details)
        print(data)

    def get_posts(self, driver):
        time_then = str(datetime.date.today() - datetime.timedelta(6 * 365 / 12))
        time_then = int(time.mktime(datetime.datetime.strptime(time_then, "%Y-%m-%d").timetuple()))
        posts = list()
        post_list = driver.find_elements_by_xpath("//div[@id = 'internship_list_container']/div")
        if len(post_list) < 2:
            return posts
        try:
            driver.find_element_by_id('no_thanks').click()
        except:
            pass
        for post in post_list:
            intern_id = post.get_attribute('internshipid')
            details = post.find_elements_by_xpath(
                '//div[@internshipid = {}]/div[@class = "individual_internship_details"]/div/table['
                '@class="table"]/tbody/tr/td'.format(
                    intern_id))
            date = details[3].text.replace("'", " ")
            date = int(time.mktime(datetime.datetime.strptime(date, "%d %b %y").timetuple()))
            title = post.find_elements_by_xpath(
                '//div[@internshipid = {}]/div[@class = "individual_internship_header"]/div[@class = '
                '"table-cell"]/h4'.format(
                    intern_id))
            link = title[0].find_element_by_tag_name('a').get_attribute('href')
            company = title[1].text
            title = title[0].text
            locations_list = [location.text for location in
                              post.find_elements_by_xpath(
                                  '//div[@internshipid = {}]/div[2]/p/span[2]/a'.format(intern_id))]
            start_Date = details[0].text
            duration = details[1].text
            stipend = details[2].text
            posts.append(
                {'_id': int(intern_id), 'Date': date, 'Title': title, 'Company': company, 'Locations': locations_list,
                 'Stipend': stipend,
                 'Start': start_Date,
                 'Time period': duration, 'link': link})
        return posts


if __name__ == '__main__':
    internshala().run()
