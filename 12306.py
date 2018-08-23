
import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class reserve(object):
    def __init__(self):
        self.login_url='https://kyfw.12306.cn/otn/login/init'
        self.username='13820016973'
        self.password='258258scpyzl'
        self.start_station='合肥'
        self.destination='天津'
        self.train_date='2018-9-12'
        self.train=['G266','G330','G304']
        self.sub=0
        self.driver=webdriver.Chrome()

    #跳转到登陆页面并且进行手动输入验证码进行登陆
    def get_url(self):
        print('[0]打开浏览器')
        self.driver.get(self.login_url)
        time.sleep(2)

    def login_12306(self):
        print('[1]进行账号登陆设置')
        self.driver.find_element_by_id('username').send_keys(self.username)
        self.driver.find_element_by_id('password').send_keys(self.password)
        print('[2]请手动点击验证码并进行登录')
        while self.login_url==self.driver.current_url:
            print('[*]请等待手工输入完成')
            time.sleep(2)
        print('登陆成功')
        # if (self.driver.current_url == 'http://www.12306.cn/mormhweb/logFiles/error.html'):
        #     self.driver.back()

    #进行车票预定
    def reserve1(self):
        print('[3]点击车票预定')
        # if (self.driver.current_url == 'http://www.12306.cn/mormhweb/logFiles/error.html'):
        #     self.driver.back()
        # WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, 'selectYuding'))).click()
        self.driver.find_element_by_xpath("//li[@id='selectYuding']/a").click()
        # if self.driver.current_url=='https://kyfw.12306.cn/otn/index/initMy12306':
        #     self.driver.find_element_by_xpath("//li[@id='selectYuding']/a").click()
        time.sleep(1)

    #进行车票查询
    def query(self):
        print('[4]点击单程和普通按钮')
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'dc'))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'sf1'))).click()
        print('进出设置配置ok')
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'fromStation_icon_image'))).click()
        self.driver.find_element_by_xpath("//li[@title='%s' and @data='HFH']" % self.start_station).click()
        # 目的地
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'toStation_icon_image'))).click()
        self.driver.find_element_by_xpath("//li[@title='%s' and @data='TJP']" % self.destination).click()
        # 出发日
        # self.driver.find_element_by_id('fromStationText').send_keys('合肥')
        # self.driver.find_element_by_id('toStationText').send_keys(self.destination)
        # WebDriverWait(self.driver, 10).until(EC.element_located_to_be_selected((By.ID, 'fromStationText'))).send_keys(self.start_station)
        # WebDriverWait(self.driver, 10).until(EC.element_located_to_be_selected((By.ID, 'toStationText'))).send_keys(self.destination)
        #进行日期自动设定
        year=self.train_date.split('-')[0]
        month=self.train_date.split('-')[1]
        day=self.train_date.split('-')[2]
        m=int(month)
        d=int(day)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'date_icon_1'))).click()
        self.driver.find_element_by_xpath("//div[@class='year']/input").click()
        self.driver.find_element_by_xpath("//div[@class='year']/div/ul/li[text()='%s']" % year).click()
        self.driver.find_element_by_xpath("//div[@class='month']/input").click()
        self.driver.find_element_by_xpath("//div[@class='month']/ul/li[%d]" % m).click()
        self.driver.find_element_by_xpath("//div[@class='cal']/div[@class='cal-cm']/div[%d]/div" % d).click()
        self.driver.find_element_by_xpath("//div[@class='btn-area']/a").click()
        time.sleep(2)

    #进行车次的数量检查
    def train_num(self):
        num=self.driver.find_element_by_id('trainum').text.strip()
        print("共有"+num+"车次")
        return  num


    #进行余票检查
    def check(self):
        #检查是否有自己需要的车次，有则观察其是否有二等座，若没有则进行下一车次搜索，反之过去
        int_num=int(self.train_num())
        list=[]
        j=0
        #将查询出的车次放入一个列表中
        for i in range(2*int_num):
            if i%2==0:
                list.append(self.driver.find_element_by_xpath("//tbody[@id='queryLeftTable']/tr[%d]/td/div/div/div/a" % (i+1)).text)
                j+=1
            else:
                pass

        #对于想要乘坐的车次和这里面进行匹配，车次二等座优先
        k=0
        for c_train in self.train:
            if c_train in list:
                index=list.index(c_train)
                two_position=self.driver.find_element_by_xpath("//tbody[@id='queryLeftTable']/tr[%d]/td[%d]" % (2*index+1,4)).text
                if two_position=='无' or two_position=='--':
                    pass
                else:
                    self.driver.find_element_by_xpath("//tbody[@id='queryLeftTable']/tr[%d]/td[%d]/a" % (2*index+1,13)).click()
                    print("车票已抢到")
                    self.sub=1
                    break

    #进行订单提交
    def pay(self):
        while self.driver.current_url!='https://kyfw.12306.cn/otn/confirmPassenger/initDc':
            pass
        self.driver.find_element_by_xpath("//input[@id='normalPassenger_3']").click()
        self.driver.find_element_by_xpath("//a[@id='submitOrder_id']").click()
        print("静待支付")




re=reserve()
re.get_url()
re.login_12306()
time.sleep(3)
re.reserve1()
re.query()
re.train_num()
while re.sub==0:
    re.check()
if re.sub==1:
    re.pay()




