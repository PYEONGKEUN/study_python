
# -*- coding: utf-8 -*- 
# selenium module
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

mobile_emulation = {

    "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },

    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }

chrome_options = Options()

chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
# bs4 module
import re
from bs4 import BeautifulSoup
import time
# convert base64 to img
import base64

import urllib.request

# file IO lib
import os
import sys
import traceback
import logging as LOGGER


LOGGER.basicConfig(filename='./log.txt', level=LOGGER.DEBUG)
class ScrapImgs:


    def __init__ (self, savePath, fileName,all_these_words= '',this_exact_word_or_phrase= '',any_of_these_words= '',none_of_these_words= ''):
        self._savePath = savePath
        self._fileName = fileName
        self._progress = 0.0
        self._all_these_words = all_these_words
        self._this_exact_word_or_phrase = this_exact_word_or_phrase
        self._any_of_these_words = any_of_these_words
        self._none_of_these_words = none_of_these_words
        self._SLEEP_TIME = 3
        self._SCROLL_SLEEP_TIME = 1
        self._SCROLL_SIZE = 1080
        #self.driver = webdriver.Chrome('.\chromedriver.exe')
        self.driver = webdriver.Chrome(chrome_options = chrome_options)


    def teardown_method(self, method):
        self.driver.quit()

    def increasePregress(self, flt):
        if self._progress < 100.0 :
            self._progress += flt
        else:
            pass

    def run(self):
        
        LOGGER.info('selenium Chrome Driver Loaded')
        LOGGER.info('waiting 3 seconds....')
        self.driver.implicitly_wait(self._SLEEP_TIME)


        desired_caps = {}
        desired_caps['testdroid_username'] = 'ville-veikko.helppi@bitbar.com'
        desired_caps['testdroid_password'] = 'xxxxxxxx'
        desired_caps['testdroid_target'] = 'chrome'
        desired_caps['testdroid_project'] = 'Appium Chrome'
        desired_caps['testdroid_testrun'] = 'TestRun 1'
        desired_caps['testdroid_device'] = 'Asus Google Nexus 7 (2013) ME571KL'
        desired_caps['platformName'] = 'android'
        desired_caps['deviceName'] = 'AndroidDevice'
        desired_caps['browserName'] = 'chrome'


        #구글 이미지 검색에 접근      
        self.driver.get('https://www.google.co.kr/imghp?hl=ko')
        #self.driver = driver.Remote('https://www.google.co.kr/imghp?hl=ko',desired_caps)
        
        time.sleep(self._SLEEP_TIME)
        # 검색
        
        self.driver.find_element(By.NAME, "q").click()
        #구글의 고급검색 기능 구현
        keyword  = ''
        #다음 단어 모두 포함:
        split_all_these_words = self._all_these_words.split(' ')
        #다음 단어 또는 문구 정확하게 포함:
        split_this_exact_word_or_phrase = self._this_exact_word_or_phrase.split(' ')
        #다음 단어 중 아무거나 포함
        split_any_of_these_words = self._any_of_these_words.split(' ')
        #다음 단어 제외
        split_none_of_these_words = self._none_of_these_words.split(' ')

        #다음 단어 모두 포함:
        if(len(split_all_these_words) > 0 and split_all_these_words[0] != ''):
            
            for index, value in enumerate(split_all_these_words,start=0):
                if(value == ''): break
                keyword += value + " "
        #다음 단어 또는 문구 정확하게 포함:
        if(len(split_this_exact_word_or_phrase) > 0 and split_this_exact_word_or_phrase[0] != ''):
            
            for index, value in enumerate(split_this_exact_word_or_phrase,start=0):
                if(value == ''): break
                if(index != len(split_this_exact_word_or_phrase)-1):
                    keyword += value + " OR "
                else:
                    keyword += value + " "
        #다음 단어 중 아무거나 포함
        if(len(split_any_of_these_words) > 0 and split_any_of_these_words[0] != ''):
            
            keyword += '"'
            for index, value in enumerate(split_any_of_these_words,start=0):
                if(value == ''): break
                if(index != len(split_any_of_these_words)-1):
                    keyword += value + " "
                else:
                    keyword += value
            keyword += '" '
        #다음 단어 제외
        if(len(split_none_of_these_words) > 0 and split_none_of_these_words[0] != ''):
            
            for index, value in enumerate(split_none_of_these_words,start=0):
                if(value == ''): break
                keyword += "-"+value + " "

        self.driver.find_element(By.NAME, "q").send_keys(keyword)
        self.driver.find_element(By.NAME, "q").send_keys(Keys.ENTER)

        
        
        #검색 결과에서 스크롤 -> 사람이 하는것처럼 딜레이를 주어 구글을 속임
        prevPageYOffset = self.driver.execute_script('return window.pageYOffset;')
        for i in range(1,100):
            self.driver.execute_script("window.scrollTo(0,"+str(i*self._SCROLL_SIZE)+")")
            if(prevPageYOffset == self.driver.execute_script('return window.pageYOffset;')):
                html = self.driver.page_source
                bsObj = BeautifulSoup(html, 'html.parser')
            
                # 검색결과 더보기 버튼은 항상 존재하지만 
                # style="display:none" style="" 로 보였다 안보였다 한다
                showMore = bsObj.find('input',{'value':'결과 더보기'})
                # regex = re.compile('none')
                # m = regex.match(showMore['style'])
                # style="display:none" 가 match 된다면 아직 보이지 않음
                # None이여야 보이는 거임 None 아닐 경우에 실행 해야함
                #if(showMore != None and m is None):
                noImages = bsObj.find('div',text='더 이상 표시할 콘텐츠가 없습니다.')
                if(noImages is not None): break
                if(showMore is not None): 
                    #self.driver.find_element_by_css_selector("input[class='ksb'][value='결과 더보기']").clcik()
                    try:
                        self.driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()
                    except:
                        None
                    try:
                        self.driver.find_element_by_xpath("/html//div[@id='islmp']//div[@class='tmS4cc']//input[@value='결과 더보기']").clcik()
                    except:
                        None

            time.sleep(self._SCROLL_SLEEP_TIME)
            prevPageYOffset = self.driver.execute_script('return window.pageYOffset;')
            
        # 이미지 소스를 가져올 페이지 복사후 selenium 크롬 종료
        html = self.driver.page_source
        self.driver.quit()

        # Beautiful Soup 으로 이미지 소스 파싱
        bsObj = BeautifulSoup(html, 'html.parser')
        imgsBase64 = bsObj.findAll('img',{'alt':re.compile(keyword),'src':re.compile('base64')})
        imgsUrl = bsObj.findAll('img',{'alt':re.compile(keyword),'src':re.compile('http')})
        


        # html에 img 태그들 수집
        for img in imgsBase64:
            with open(self._fileName+'.html', 'a', encoding='utf-8') as file:
                file.writelines(str(img))
        for img in imgsUrl:
            with open(self._fileName+'.html', 'a', encoding='utf-8') as file:
                file.writelines(str(img))
        
        #다운해야할 파일 갯수 계산 & process increase 값 설정
        totalSize = len(imgsBase64) + len(imgsUrl)
        stepSize = 100.0 / totalSize
        

        # 이미지 다운로드
        num = 0
        for img in imgsBase64:
            with open(self._fileName+'_'+str(num)+'.jpg', 'wb') as file:
                file.write(base64.b64decode(str(img['src']).split(',')[1]))
            num+=1
            self.increasePregress(stepSize)
            print('##progress : '+'{:04.2f}%' .format(self._progress))
        
        for img in imgsUrl:
            
            urllib.request.urlretrieve(str(img['src']),self._fileName+'_'+str(num)+'.jpg')
            num+=1
            self.increasePregress(stepSize)
            print('##progress : '+'{:04.2f}%' .format(self._progress))

        
        













if __name__ == '__main__':
    app = ScrapImgs('./','엄지','엄지','여자친구','','손가락 손톱 지문 손금 손바닥 손')
    app.run()