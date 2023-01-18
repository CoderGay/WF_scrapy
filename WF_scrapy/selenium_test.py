from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# 创建 WebDriver 对象，指明使用chrome浏览器驱动
wd = webdriver.Chrome(service=Service(r'e:\tools\chromedriver.exe'))

# 调用WebDriver 对象的get方法 可以让浏览器打开指定网址
# wd.get('https://c.wanfangdata.com.cn/periodical')

# wd.get('https://image.baidu.com/')
#
# try:
#     # 根据id选择元素，返回的就是该元素对应的WebElement对象
#     element = wd.find_element(By.ID, 'kw')
#     # 通过该 WebElement对象，就可以对页面元素进行操作了
#     # 比如输入字符串到 这个 输入框里
#     keywords = ['江西师范大学']
#     element.send_keys(keywords[0] + '\n')
# except NoSuchElementException as e:
#     print(e.msg)
#     pass
#
# wd.quit()


def seleniumGet(url):
    wd.get(url)
    try:
        element_btn = wd.find_element(By.CLASS_NAME, 'slot-box')
        element_btn.click()
    except NoSuchElementException as err:
        print(err.msg)
        print('===>' + url)
        pass

    try:
        element_summary = wd.find_element(By.XPATH, ".//div[@class='summary list']//span[@class='text-overflow']/span")
        print(element_summary.text)
    except NoSuchElementException as err:
        print(err.msg)
        pass
    print('Test Open finished')
    # input()
    # wd.quit()


test_url = 'https://d.wanfangdata.com.cn/periodical/jsjxb202210001'
seleniumGet(test_url)
