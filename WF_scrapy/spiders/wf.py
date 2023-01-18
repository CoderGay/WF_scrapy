import time

import scrapy

import json
import random

from WF_scrapy import selenium_test
from WF_scrapy.items import PaperItem
from WF_scrapy.asyncSpider.PeriodicalAjax2Spider import PeriodicalAjax2Spider
from WF_scrapy.selenium_dataLoader.SeleniumDataLoader import SeleniumDataLoader
from WF_scrapy.user_agents import agents
from WF_scrapy.pojo.Paper import Paper
from WF_scrapy.dao import ItemDAO

oldestPublishYear = 2018

limitNum = 10


class WfSpider(scrapy.Spider):
    name = 'wf'  # 爬虫唯一识别名称
    # 搜索的限制域名，超过此域名的不会爬，可选参数(可以注释掉不写)
    allowed_domains = ['wanfangdata.com.cn', 'c.wanfangdata.com.cn', 'sns.wanfangdata.com.cn', 'd.wanfangdata.com.cn']
    # 第一次下载数据会从以下url开始
    start_urls = ['https://c.wanfangdata.com.cn/periodical', 'http://c.wanfangdata.com.cn/']
    # config your oldest publish year

    # TODO 还待手工收集持续完善,当然你也可以仿造PeriodicalAjax2Spider.py进行自动爬取(不建议)
    url_params_dict = {
                    # '哲学政法': ['B_B0', 'B_B80', 'B_B84', 'B_B9', 'B_BA', 'B_BAA', 'B_BD', 'B_BD2', 'B_BD8', 'B_BD9'],
                    # '社会科学': ['C_C0', 'C_C91', 'C_C913', 'C_C92', 'C_C97', 'C_CA', 'C_CK0', 'C_CK9'],
                    # '经济财政': ['F_F0', 'F_F2', 'F_F3', 'F_F4', 'F_F5', 'F_F6', 'F_F7', 'F_F8', 'F_FA'],
                    # '教科文艺': ['G_G0', 'G_G21', 'G_G25', 'G_G3', 'G_G4', 'G_G61', 'G_G63', 'G_G8', 'G_GA', 'G_GH',
                    #             'G_GI', 'G_GJ'],
                    # '基础科学': ['N_NA', 'N_N01', 'N_N03', 'N_N04', 'N_N06', 'N_NP', 'N_NQ', 'N_NT'],
                    '医药卫生': ['R_R1', 'R_R16', 'R_R2', 'R_R3', 'R_R4', 'R_R5', 'R_R6', 'R_R71', 'R_R73', 'R_R74', 'R_R75', 'R_R76', 'R_R8', 'R_R9', 'R_RA', 'R_RT'],
                    '农业科学': ['S_S1', 'S_S2', 'S_S3', 'S_S4', 'S_S5', 'S_S6', 'S_S7', 'S_S8', 'S_S9', 'S_SA', 'S_ST'],
                    '工业技术': ['T_TA', 'T_TB', 'T_TD', 'T_TE', 'T_TF', 'T_TG', 'T_TH', 'T_TJ', 'T_TK', 'T_TL', 'T_TM', 'T_TN', 'T_TP', 'T_TQ', 'T_TS', 'T_TU', 'T_TV', 'T_TX', 'T_TY', 'T_TZ']}

    # '哲学政法', '社会科学', '经济财政', '教科文艺', '基础科学', '医药卫生', '农业科学', '工业技术'
    url_params_keywords = ['医药卫生', '农业科学', '工业技术']

    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)
        # self.MagazineNumTotal = 0
        self.cnt = 0
        self.perRequestItemNums = 20
        self.magazineItemIdList = []
        self.magazineItemBaseUrl = "https://c.wanfangdata.com.cn/Category/Magazine/search"

    def start_requests(self):

        # TODO 如何迭代着爬取

        for keyword in self.url_params_keywords:
            for url_param in self.url_params_dict[keyword]:
                url = "https://c.wanfangdata.com.cn/periodical?class_code={}".format(url_param)
                # TODO
                # idGenerator = PeriodicalAjax2Spider(url)
                WfSpider.custom_settings = self.getDefaultRequestHeaders(url)
                # # TODO Delay Limited
                # time.sleep(3)
                # 使用yield多线程发起请求
                yield self.getPeriodicalItemId(url, scrapy)

                # TODO :还待完善
                yield scrapy.Request(url=url)

    # 解析的方法, 每个初始URL完成下载后将会被调用,调用的时候传入每一个URL返回的Response对象来作为唯一参数
    def parse(self, response):
        # print(str(response.body.decode("utf-8")))
        # print('come in')
        pass
        # items = []
        # 1.负责解析返回的网页数据(response.body)，提取结构化数据(生成item)

        # //div[@class='detailTitleCN']/span[@class='']  # 伦理与道德:谁是优先战略
        # // wf-article-list//wf-article-item//a//@href  # https://d.wanfangdata.com.cn/periodical/llxyj202205012 #     Author : 林俊杰  # Date: 2023/1/3
        # 2.生成需要下一页的URL请求

        # if len(response.xpath("//a[@class='noactive' and @id='next']")) == 0:  # 到了最后一页
        #     url = response.xpath("//a[@id='next']/@href").extract_first()[0]  # 提取新的url
        #     yield scrapy.Request(url, callback=self.parse)  # 发起请求

    # def parse_model(self, response):
    #     print("parse_model============================>\n" + str(response.body.decode("utf-8")))

    def getDefaultRequestHeaders(self, referer):
        custom_settings = {
            "DEFAULT_REQUEST_HEADERS": {
                'authority': 'c.wanfangdata.com.cn',
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'origin': 'https://c.wanfangdata.com.cn',
                'referer': referer,
                'user-agent': random.choice(agents),
                'Content-Type': 'application/json',
            }
        }
        return custom_settings

    def getPeriodicalItemId(self, referer, scrapyParam=None, curIndex=0):
        if scrapyParam is None:
            raise ValueError("Scrapy必须传进来,因为需要通过Scrapy.Request()发起Ajax异步请求")
        # 网页里ajax链接
        url = self.magazineItemBaseUrl
        # 所有请求集合
        requests = []
        # self.refresh_request_payload(curIndex)
        class_code = referer.split('_')[-1]
        request_payload = {
            "query": [],
            "start": curIndex,
            "rows": self.perRequestItemNums,
            "sort_field": {
                "sort_field": "LastYear;HasFulltext;CoreScore"
            },
            "highlight_field": "",
            "pinyin_title": [],
            "class_code": class_code,
            "core_periodical": [],
            "sponsor_region": [],
            "publishing_period": [],
            "publish_status": "",
            "return_fields": [
                "Title",
                "Id",
                "CorePeriodical",
                "Award",
                "IsPrePublished"
            ]
        }
        # 先去刺探军情:
        request = scrapyParam.Request(url, method='POST', callback=self.parse_magazine,
                                      body=json.dumps(request_payload),
                                      encoding='utf-8')

        # TODO 步入正题
        # lastIndex = self.MagazineNumTotal / 20
        # for i in range(1, 1):
        #     pass

        # requests.append(request)
        # return requests

        return request

    # 解析杂志的post请求响应
    def parse_magazine(self, response):
        jsonBody = json.loads(response.body.decode("utf-8"))

        for item in jsonBody['value']:
            # # TODO limited
            # if self.cnt >= limitNum:
            #     break
            magazineItemId = item['Id']
            self.magazineItemIdList.append(magazineItemId)
            magazineUrl = "https://sns.wanfangdata.com.cn/perio/{}".format(str(magazineItemId))
            # 编写get请求, 获取某指定期刊的页面,下一步就是打开期刊的文章的标题链接, 由parse_magazine_detail函数解析
            magazineItem_request = scrapy.Request(magazineUrl, method='GET', callback=self.parse_magazine_detail,
                                                  encoding='utf-8')
            # # TODO Delay Limited
            # time.sleep(10)
            # 发起请求
            yield magazineItem_request
        magazineNumTotal = int(jsonBody['total'])

        url = self.magazineItemBaseUrl

        class_code = json.loads(response.request.body.decode("utf-8"))['class_code']
        # print('class_code xxxxxxxxxxxxxxxxxx>')
        # print(class_code)

        lastIndex = (magazineNumTotal // 20) + 1
        # print('total = {}, lastIndex = {}'.format(magazineNumTotal, lastIndex))
        for i in range(1, lastIndex):
            # # TODO limited
            # if self.cnt >= limitNum:
            #     break
            # self.refresh_request_payload(i)
            rows = self.perRequestItemNums
            if i == lastIndex - 1:
                rows = magazineNumTotal - (self.perRequestItemNums * (lastIndex - 1))
            request_payload = {
                "query": [],
                "start": i * self.perRequestItemNums,
                "rows": rows,
                "sort_field": {
                    "sort_field": "LastYear;HasFulltext;CoreScore"
                },
                "highlight_field": "",
                "pinyin_title": [],
                "class_code": class_code,
                "core_periodical": [],
                "sponsor_region": [],
                "publishing_period": [],
                "publish_status": "",
                "return_fields": [
                    "Title",
                    "Id",
                    "CorePeriodical",
                    "Award",
                    "IsPrePublished"
                ]
            }
            # print("range:" + str(request_payload['start']) + '~' + str(
            #     request_payload['start'] + request_payload['rows']))
            # 继续模拟发起异步Post请求,获取期刊杂志的链接
            request = scrapy.Request(url, method='POST', callback=self.parse_magazine,
                                     body=json.dumps(request_payload),
                                     encoding='utf-8')
            # # TODO Delay Limited
            # time.sleep(20)
            yield request

        # print("List============================>\n")
        # print(len(self.magazineItemIdList))
        # print(self.magazineItemIdList)

        # print("List============================>\n")
        # print(self.magazineItemIdList)
        # return self.magazineItemIdList
        # self.total = response

    # 解析获取期刊的每一期的链接
    def parse_magazine_detail(self, response):
        # TODO 下面分别为左侧栏和分页
        # "//wf-field-value/span/@data-href"  # 左侧栏-第几期
        # "//wf-pagination//li/a/@href"  # 下一页
        issueNum_base_url = "https://sns.wanfangdata.com.cn"
        # paperItems = []
        issueNum_list = response.xpath("//wf-issue-list//wf-field-value/span")
        # 第几期
        flag = 0
        for issueNum_element in issueNum_list:
            # TODO limited
            # if self.cnt >= limitNum:
            #     break
            # /sns/perio/jsjxb/?tabId=article&publishYear=2022&issueNum=11&page=1&isSync=0
            issueNum_link = issueNum_element.xpath("./@data-href").extract_first()
            # print(issueNum_link)
            publishYear = int(str(issueNum_link).split('publishYear=')[1][0:4])
            if publishYear < oldestPublishYear or flag == 1:
                continue  # 太久远的不收集
            # issueNum_link只有uri位置并没有base_url, 给它concat一下
            flag = 1
            issueNum_url = issueNum_base_url + issueNum_link
            # 获取下一页的连接,因为有"下一页"按钮的<a>标签,故pageNum_list的元素个数刚好是页数
            pageNum_list = response.xpath("//wf-pagination//li/a")
            curPage = 0
            for pageNum_element in pageNum_list:
                # 这个链接没啥用,先放这,跟上面一样,都没有base_url
                curPage = curPage + 1
                pageNum_link = str(pageNum_element.xpath("./@href").extract_first()).split('page=')[0]+str(curPage)
                pageNum_url = issueNum_base_url + pageNum_link
                # title_list = response.xpath("//wf-article-item//a")
                #
                # for title_element in title_list:
                #     title = title_element.xpath(".//h2/text()").extract_first()
                #     paperUrl = title_element.xpath("./@href").extract_first()
                #     print(title)
                #     print(paperUrl)
                #     # selenium_test.seleniumGet(paperUrl)
                #     dataLoader = SeleniumDataLoader()
                #     paperObject = dataLoader.seleniumGet(paperUrl)
                #     print('最终结果')
                #     print(paperObject)
                #     paper_item = ItemDAO.convertPaperItem(paperObject)
                #     # with open('./test1.txt', 'w', encoding='utf-8') as f:
                #     #     print(paperObject, file=f)
                #     paperItems.append(paper_item)
                article_request = scrapy.Request(pageNum_url, method='GET', callback=self.parse_article_detail,
                                                    encoding='utf-8')
                # TODO Delay Limited
                # time.sleep(30)
                # 使用yield多线程发起请求
                yield article_request

    def parse_article_detail(self, response):
        paperItems = []
        title_list = response.xpath("//wf-article-item//a")
        dataLoader = SeleniumDataLoader()

        for title_element in title_list:
            title = title_element.xpath(".//h2/text()").extract_first()
            paperUrl = title_element.xpath("./@href").extract_first()
            print(title)
            print(paperUrl)
            # selenium_test.seleniumGet(paperUrl)
            # TODO Delay Limited
            # time.sleep(30)
            paperObject = dataLoader.seleniumGet(paperUrl)
            # print('最终结果')
            # print(paperObject)
            paper_item = ItemDAO.convertPaperItem(paperObject)
            paperItems.append(paper_item)
            self.cnt = self.cnt + 1  # nothing
            yield paper_item
        dataLoader.seleniumClose()
