#python3
"""
在丁香园网站获取新型冠状病毒疫情实时数据。2020-02-22
"""


import myscrap
import pandas as pd
import time
import lxml.html as lh

#存储全国疫情数据
yiqing = {'xcqz': 0, 'xcys': 0, 'xczz': 0, 'ljqz': 0, 'ljsw': 0, 'ljzy': 0}

def parseYiqing_national(html):
    """
    解析全国疫情数据
    """

    tree = lh.fromstring(html)
    datas = tree.xpath('//ul[@class="count___3GCdh multRow___j004q"]/li')
    xcqz = datas[0].xpath('./strong')[0].text_content()
    xcys = datas[1].xpath('./strong')[0].text_content()
    xczz = datas[2].xpath('./strong')[0].text_content()
    ljqz = datas[3].xpath('./strong')[0].text_content()
    ljsw = datas[4].xpath('./strong')[0].text_content()
    ljzy = datas[5].xpath('./strong')[0].text_content()

    yiqing['xcqz'] = int(xcqz)
    yiqing['xcys'] = int(xcys)
    yiqing['xczz'] = int(xczz)
    yiqing['ljqz'] = int(ljqz)
    yiqing['ljsw'] = int(ljsw)
    yiqing['ljzy'] = int(ljzy)


class Yiqing:
    """
    各地区疫情数据
    """
    def __init__(self, area, xcqz, ljqz, sw, zy):
        self.xcqz = xcqz
        self.ljqz = ljqz
        self.sw = sw
        self.zy = zy
        self.area = area

    def __str__(self):
        return "现存确诊 %s 人, 累计确诊 %s 人, 死亡 %s 人, 治愈 %d 人。" \
               % (self.xcqz, self.ljqz, self.sw, self.zy)


def parseYiqing_area(html):
    """
    解析各地区疫情数据
    返回一个字典：data: 全省的数据; 省名称：各地级市 的数据
    """
    tree = lh.fromstring(html)
    areas = tree.xpath('//div[@class="fold___xVOZX"]')
    province = []  # 全省的疫情数据
    for area in areas:
        p = area.xpath('./div[@class="areaBlock1___3V3UU"]')  # 省
        cs = area.xpath('./div[@class="areaBlock2___27vn7"]')  # 城市

        data_p = p[0].xpath('./p')
        pname = data_p[0].text_content()
        yq = Yiqing(pname, data_p[1].text_content(),
                    data_p[2].text_content(), data_p[3].text_content(), data_p[4].text_content())
        #province['data'] = yq  # 省级疫情数据
        province.append(yq)

        yiqing_c = []  # 某个省内所有城市的疫情数据
        for city in cs:
            data_c = city.xpath('./p')
            if len(data_c) != 4:
                continue

            yq = Yiqing(data_c[0].text_content(), data_c[1].text_content(),
                        data_c[2].text_content(), data_c[3].text_content(), data_p[4].text_content())
            #yiqing_c.append(yq)
            province.append(yq)

        #province[pname] = yiqing_c

    # 返回数据
    return province


def write_national_data_tofile(yiqing_national):
    print(yiqing_national)

    # 写的数据前，添加时间信息
    yiqing_national['date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    df = pd.DataFrame(yiqing_national, index=[yiqing_national['date']])
    df.to_csv('yiqing2.csv', mode='a+', header=False, index=False)


def write_area_data_tofile(data):
    """
    将列表疫情数据写入文件
    [Yiqing,Yiqing] ==> [area, qz, sw, zy]
    @param yiqing:
    @return: None
    """
    print(yiqing)

    # 写数据前，添加时间信息
    all = []
    for yq in data:
        yqing = {'城市': yq.area, '现存确诊': yq.xcqz, '累计确诊': yq.ljqz, '死亡':yq.sw, '治愈': yq.zy}
        yqing['更新时间'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        all.append(yqing)

    df = pd.DataFrame(all, index=None)
    df.to_csv('yiqingarea2.csv', mode='a+', header=False, index=False)


if __name__ == "__main__":
    print('start to getting data...')

    from apscheduler.schedulers.background import BackgroundScheduler

    url = r'https://ncov.dxy.cn/ncovh5/view/pneumonia_peopleapp?from=timeline&isappinstalled=0'
    # count = 1

    """
    html = myscrap.getDinamicPageSource(url)
    parseYiqing_national(html)
    province = parseYiqing_area(html)
    write_national_data_tofile(yiqing)
    write_area_data_tofile(province)
    print('get data successed.')

    """


    def getTheData():
        html = myscrap.getDinamicPageSource(url)
        parseYiqing_national(html)
        province = parseYiqing_area(html)
        write_national_data_tofile(yiqing)
        write_area_data_tofile(province)
        print('get data successed for at %s.' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # count += 1


    scheduler = BackgroundScheduler()
    scheduler.add_job(getTheData, 'interval', hours=1, start_date='2020-02-04 20:00:01', end_date='2020-06-30 23:23:23')
    scheduler.start()

    while True:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        time.sleep(3500)
