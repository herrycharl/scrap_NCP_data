#python3
"""
获取页面数据
"""


def getDinamicPageSource(url):
    """
    使用浏览器模拟的方式获取动态页面数据
    """
    from selenium import webdriver
    browser = webdriver.Firefox()

    browser.get(url)
    return browser.page_source


def getStaticPageSource(url):
    """
    直接获取静态页面数据
    """
    import urllib3
    http = urllib3.PoolManager()
    urllib3.disable_warnings()
    page = http.request('GET', url)
    return page.data.decode()


if __name__ == "__main__":
    url = r'https://ncov.dxy.cn/ncovh5/view/pneumonia_peopleapp?from=timeline&isappinstalled=0'
    html = getDinamicPageSource(url)
    html2 = getStaticPageSource(url)

    f = open('html.txt', 'w', encoding='utf-8')
    f.write(html)
    f.close()
    f = open('html2.txt', 'w', encoding='utf-8')
    f.write(html2)
    f.close()
    print('Done!')
