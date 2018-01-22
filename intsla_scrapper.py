from selenium import webdriver
import datetime, time
import csv


class internshala():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.file = open('intern_info.csv', 'w')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['Date Posted', 'Title', 'Company', 'Locations', 'Stipend', 'Start Date', 'Duration'])
        self.url = 'https://internshala.com/internships/python%2Fdjango-internship'
        self.driver.get('https://internshala.com/internships/python%2Fdjango-internship')

    def run(self, is_csv):
        data = self.get_posts(self.driver)
        print(data)
        self.driver.close()
        if is_csv:
            for post in data:
                self.writer.writerow(post)
        else:
            return data

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
            company = title[1].text
            title = title[0].text
            locations_list = [location.text for location in
                              post.find_elements_by_xpath(
                                  '//div[@internshipid = {}]/div[2]/p/span[2]/a'.format(intern_id))]
            start_Date = details[0].text
            duration = details[1].text
            stipend = details[2].text
            posts.append([date, title, company, locations_list, stipend, start_Date, duration])
        return posts


if __name__ == '__main__':
    internshala().run(True)
