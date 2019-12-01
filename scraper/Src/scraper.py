
# -*- coding: utf-8 -*- 
# selenium module
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
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
        self.driver = webdriver.Chrome('.\chromedriver.exe')



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

        #구글 이미지 검색에 접근      
        self.driver.get('https://www.google.co.kr/imghp?hl=ko')
        header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        time.sleep(self._SLEEP_TIME)
        # 검색 키워드 생성
        self.driver.find_element(By.NAME, "q").click()

        keyword  = ''
        split_all_these_words = self._all_these_words.split(' ')
        split_this_exact_word_or_phrase = self._this_exact_word_or_phrase.split(' ')
        split_any_of_these_words = self._any_of_these_words.split(' ')
        split_none_of_these_words = self._none_of_these_words.split(' ')


        if(len(split_all_these_words) > 0 and split_all_these_words[0] != ''):
            
            for index, value in enumerate(split_all_these_words,start=0):
                if(value == ''): break
                keyword += value + " "

        if(len(split_this_exact_word_or_phrase) > 0 and split_this_exact_word_or_phrase[0] != ''):
            
            for index, value in enumerate(split_this_exact_word_or_phrase,start=0):
                if(value == ''): break
                if(index != len(split_this_exact_word_or_phrase)-1):
                    keyword += value + " OR "
                else:
                    keyword += value + " "
        if(len(split_any_of_these_words) > 0 and split_any_of_these_words[0] != ''):
            
            keyword += '"'
            for index, value in enumerate(split_any_of_these_words,start=0):
                if(value == ''): break
                if(index != len(split_any_of_these_words)-1):
                    keyword += value + " "
                else:
                    keyword += value
            keyword += '" '
        if(len(split_none_of_these_words) > 0 and split_none_of_these_words[0] != ''):
            
            for index, value in enumerate(split_none_of_these_words,start=0):
                if(value == ''): break
                keyword += "-"+value + " "

        self.driver.find_element(By.NAME, "q").send_keys(keyword)
        self.driver.find_element(By.NAME, "q").send_keys(Keys.ENTER)

        
        

        num = 0
        for i in range(1,20):
            self.driver.execute_script("window.scrollTo(0,"+str(i*self._SCROLL_SIZE)+")")
            time.sleep(self._SCROLL_SLEEP_TIME)
            
        # 이미지 소스를 가져올 페이지 복사후 selenium 크롬 종료
        html = self.driver.page_source
        self.driver.quit()

        bsObj = BeautifulSoup(html, 'html.parser')
        # loadButton = bsObj.find('smc',{'style':re.compile('none')})
        # if loadButton is None:
        #     self.driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()
        # 이미지 src 수집
        imgsBase64 = bsObj.findAll('img',{'alt':re.compile(keyword),'src':re.compile('base64')})
        imgsUrl = bsObj.findAll('img',{'alt':re.compile(keyword),'src':re.compile('http')})
        
        totalSize = len(imgsBase64) + len(imgsUrl)
        stepSize = 100.0 / totalSize

        # html에 이미지 수집
        for img in imgsBase64:
            with open('output.html', 'a', encoding='utf-8') as file:
                file.writelines(str(img))
        for img in imgsUrl:
            with open('output.html', 'a', encoding='utf-8') as file:
                file.writelines(str(img))
        
        

        # 이미지 다운로드
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