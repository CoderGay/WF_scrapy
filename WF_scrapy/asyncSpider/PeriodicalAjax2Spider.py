import json
import random
import scrapy
from WF_scrapy.user_agents import agents


class PeriodicalAjax2Spider:
    #  custome_setting可用于自定义每个spider的设置，而setting.py中的都是全局属性的，当你的
    #  scrapy工程里有多个spider的时候这个custom_setting就显得很有用了
    def __init__(self, referer_params="https://c.wanfangdata.com.cn/periodical?class_code=T_TP"):
        self.referer = referer_params
        self.magazineItemBaseUrl = "https://c.wanfangdata.com.cn/Category/Magazine/search"
        self.perRequestItemNums = 20
        self.class_code = self.referer.split('_')[-1]
        self.magazineItemIdList = []

    def getDefaultRequestHeaders(self):
        custom_settings = {
            "DEFAULT_REQUEST_HEADERS": {
                'authority': 'c.wanfangdata.com.cn',
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'origin': 'https://c.wanfangdata.com.cn',
                # 表示这个请求是从哪个URL过来的，原始资源的URI
                'referer': self.referer,
                # 设置请求头信息User-Agent来模拟浏览器
                'user-agent': random.choice(agents),
                # 'x-requested-with': 'XMLHttpRequest',
                # cookie也是报文属性，传输过去
                # 'cookie': 'cna=/oN/DGwUYmYCATFN+mKOnP/h; tracknick=adimtxg; _cc_=Vq8l%2BKCLiw%3D%3D; tg=0; thw=cn; v=0; cookie2=1b2b42f305311a91800c25231d60f65b; t=1d8c593caba8306c5833e5c8c2815f29; _tb_token_=7e6377338dee7; CNZZDATA30064598=cnzz_eid%3D1220334357-1464871305-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1464871305; CNZZDATA30063600=cnzz_eid%3D1139262023-1464874171-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1464874171; JSESSIONID=8D5A3266F7A73C643C652F9F2DE1CED8; uc1=cookie14=UoWxNejwFlzlcw%3D%3D; l=Ahoatr-5ycJM6M9x2/4hzZdp6so-pZzm; mt=ci%3D-1_0',
                # 就是告诉服务器我参数内容的类型
                'Content-Type': 'application/json',
            }
        }
        return custom_settings

    def getPeriodicalItemId(self, scrapyParam=None):
        if scrapyParam is None:
            raise ValueError("Scrapy必须传进来,因为需要通过Scrapy.Request()发起Ajax异步请求")
        # 网页里ajax链接
        url = self.magazineItemBaseUrl
        # 所有请求集合
        requests = []
        curIndex = 0
        request_payload = {
            "query": [],
            "start": curIndex,
            "rows": self.perRequestItemNums,
            "sort_field": {
                "sort_field": "LastYear;HasFulltext;CoreScore"
            },
            "highlight_field": "",
            "pinyin_title": [],
            "class_code": self.class_code,
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
        request = scrapyParam.Request(url, method='POST', callback=self.parse_model, body=json.dumps(request_payload),
                                      encoding='utf-8')
        # requests.append(request)
        # return requests
        return request

        # TODO 步入正题
        # lastIndex = total / 20
        # for i in range(1, 1):
        #     pass

    def parse_model(self, response):

        jsonBody = json.loads(response.body.decode("utf-8"))
        print("json============================>\n")
        print(jsonBody)
        for item in jsonBody['value']:
            self.magazineItemIdList.append(item['Id'])
        # print("List============================>\n")
        # print(self.magazineItemIdList)
        # return self.magazineItemIdList
        # self.total = response

    # 需要重写start_requests方法

# def start_requests(self):
#     # 网页里ajax链接
#     url = "http://gs.amac.org.cn/amac-infodisc/api/pof/manager?"
#     # 所有请求集合
#     requests = []
#     # 这里只模拟一页range(0, 1)
#     for i in range(0, 1):
#         random_random = random.random()
#         # 封装post请求体参数
#         my_data = {'page': '111', 'size': '20', 'rand': str(random_random)}
#         # 模拟ajax发送post请求
#         request = scrapy.Request(url, method='POST',
#                                  callback=self.parse_model,
#                                  body=json.dumps(my_data),
#                                  encoding='utf-8')
#         requests.append(request)
#     return requests


# def parse_model(self, response):
#     # 可以利用json库解析返回来得数据，在此省略
#     jsonBody = json.loads(response.body)
#     # 拿到数据，再处理就简单了。不再赘述
#     pass
