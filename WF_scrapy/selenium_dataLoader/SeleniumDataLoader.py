from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from WF_scrapy.pojo.Paper import Paper
from WF_scrapy.pojo.Author import Author
from WF_scrapy.pojo.Affiliation import Affiliation
from WF_scrapy.pojo.Classification import Classification
from WF_scrapy.pojo.Keyword import Keyword
from WF_scrapy.pojo.Fund import Fund

import random

from WF_scrapy.tools import authorAdapter
from WF_scrapy.user_agents import agents


class SeleniumDataLoader:
    def __init__(self):
        # 加上参数，禁止 chromedriver 日志写屏
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        user_agent = random.choice(agents)
        options.add_argument('user-agent=%s' % user_agent)
        # 创建 WebDriver 对象，指明使用chrome浏览器驱动
        # TODO 使用你本地路径的ChromeDrive存放位置
        self.wd = webdriver.Chrome(service=Service(r'e:\tools\chromedriver.exe'), options=options)

    def getElementByXpath(self, xpath) -> WebElement:
        try:
            element = self.wd.find_element(By.XPATH, xpath)
            return element
        except NoSuchElementException as err:
            # print(err.msg)
            return None

    def getElementsByXpath(self, xpath) -> List[WebElement]:
        try:
            elements = self.wd.find_elements(By.XPATH, xpath)
            return elements
        except NoSuchElementException as err:
            # print(err.msg)
            return None

    def seleniumClose(self):
        self.wd.close()

    def seleniumGet(self, url):
        self.wd.get(url)
        try:
            element_btn = self.wd.find_element(By.CLASS_NAME, 'slot-box')
            element_btn.click()
        except NoSuchElementException as err:
            # print(err.msg)
            # print('===>' + url)
            pass

        try:
            # 单个html元素

            element_summary = self.getElementByXpath(".//div[@class='summary list']//span[@class='text-overflow']/span")
            element_title = self.getElementByXpath(".//div[@class='detailTitleCN']/span")
            element_DOI = self.getElementByXpath(".//div[@class='doiStyle']/a")
            element_update_time = self.getElementByXpath(".//div[@class='publish list']//div[@class='itemUrl']")
            element_page = self.getElementByXpath("//div[@class='pages list']/div")
            # html元素列表
            element_authors = self.getElementsByXpath(".//div[@class='author detailTitle']/div/a/span")
            element_affiliations = self.getElementsByXpath("//div[@class='organization detailOrganization']/div/span/span")
            element_classifications = self.getElementsByXpath("//div[@class='classify list']/div/span/span")
            element_keywords = self.getElementsByXpath("//div[@class='keyword list']/div/a/span")
            element_funds = self.getElementsByXpath("//div[@class='fund list']/div/span/a")


            DOI = None
            summary = None
            paper_url = None
            pages = None
            authors = []
            affiliations = []
            classifications = []
            keywords = []
            funds = []
            if element_affiliations is not None:
                for element_affiliation in element_affiliations:
                    affiliation = Affiliation(element_affiliation.text)
                    # print('affiliation:' + element_affiliation.text)
                    affiliations.append(affiliation)

            if element_authors is not None:
                for element_author in element_authors:
                    author = Author(element_author.text)
                    # print('author:' + element_author.text)
                    authors.append(author)
            authors = authorAdapter.convertAuthor(authorList=authors, affiliationList=affiliations)
            if element_classifications is not None:
                for element_classification in element_classifications:
                    content = str(element_classification.text)
                    classification = Classification(content)
                    classifications.append(classification)
            if element_keywords is not None:
                for element_keyword in element_keywords:
                    keyword = Keyword(element_keyword.text)
                    keywords.append(keyword)
            if element_funds is not None:
                for element_fund in element_funds:
                    fund = Fund(element_fund.text)
                    funds.append(fund)
            if element_DOI is not None:
                DOI = element_DOI.text
                paper_url = element_DOI.get_attribute('href')
                # print('DOI_url = ' + element_DOI.get_attribute('href'))
            if element_title is not None:
                title = element_title.text
            if element_summary is not None:
                summary = element_summary.text
                # print(element_summary.text)
            if element_page is not None:
                pages = element_page.text
            if element_update_time is not None:
                latest_update_time = str(element_update_time.text).split('(')[0]
            curPaper = Paper(DOI=DOI, title=title, abstract=summary,
                             latest_update_time=latest_update_time, paper_url=paper_url,
                             authors=authors, classification=classifications, fund=funds, keywords=keywords,
                             pages=pages)
            # self.wd.close()
            return curPaper

        except NoSuchElementException as err:
            print(err.msg)
            print('===>' + url)
            # self.wd.close()
            pass
        # print('Open finished')
