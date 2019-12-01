
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
    def __init__ (self, keyword, savePath):
        self._savePath = savePath
        self._progress = 0.0
        self._keyword = keyword
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
        
        self.driver.find_element(By.NAME, "q").click()
        self.driver.find_element(By.NAME, "q").send_keys(self._keyword)
        self.driver.find_element(By.NAME, "q").send_keys(Keys.ENTER)

        
        

        num = 0
        for i in range(1,20):
            self.driver.execute_script("window.scrollTo(0,"+str(i*self._SCROLL_SIZE)+")")
            time.sleep(self._SCROLL_SLEEP_TIME)
            
        
        html = self.driver.page_source
        
        bsObj = BeautifulSoup(html, 'html.parser')
        # loadButton = bsObj.find('smc',{'style':re.compile('none')})
        # if loadButton is None:
        #     self.driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()
        imgsBase64 = bsObj.findAll('img',{'alt':re.compile(self._keyword),'src':re.compile('base64')})
        imgsUrl = bsObj.findAll('img',{'alt':re.compile(self._keyword),'src':re.compile('http')})
        
        for img in imgsBase64:
            with open('output.html', 'a', encoding='utf-8') as file:
                file.writelines(str(img))
        
        for img in imgsBase64:
            with open(self._keyword+'_'+str(num)+'.jpg', 'wb') as file:
                file.write(base64.b64decode(str(img['src']).split(',')[1]))
            num+=1

        for img in imgsUrl:
            with open('output.html', 'a', encoding='utf-8') as file:
                file.writelines(str(img))
        
        for img in imgsUrl:
            
            urllib.request.urlretrieve(str(img['src']),self._keyword+'_'+str(num)+'.jpg')
            num+=1
        self.driver.quit()



            # imgs = bsObj.findAll('img',{'alt':re.compile(self._keyword),'src':re.compile('base64')})
            # #imgs = bsObj.findAll('img',{'class':'rg_ic'})
            
            
            # for img in imgs:
            #     with open(self._keyword+'_'+str(num)+'.jpg', 'wb') as file:
            #         file.write(base64.b64decode(str(img['src']).split(',')[1]))
            # num+=1

        
        
        '''
        for img in imgs:
            print(str(img['src']).split(','))
        '''
        '''
        with open('output.txt', 'w') as file:
            for img in imgs:
                file.writelines(str(img))
        '''
        # num = 0
        # for img in imgs:
        #     with open(self._keyword+'_'+str(num)+'.jpg', 'wb') as file:
        #         file.write(base64.b64decode(str(img['src']).split(',')[1]))
        #     num+=1
                
            
            # 구글 이미지의 미리 보기 페이지의 사진들은 src='data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABA~ 같은 형식임' 

        #<input jsaction="Pmjnye" class="mye4qd" type="button" value="결과 더보기">
        #
            # <div style="display: none;" id="smc">
            #     <div id="smbw"> <input class="ksb" value="결과 더보기" id="smb" data-lt="로드 중..." type="button"
            #     data-ved="0ahUKEwjyu-j6zZTmAhUFw4sBHRJzCgMQxdoBCLYB"> </div>
            # </div>
                # for i in range(1,10):
        #     self.driver.execute_script("window.scrollTo(0,"+str(i*scrollSize)+")")

        #     self.driver.implicitly_wait(self._SLEEP_TIME)
        #     html = self.driver.page_source
            
        #     bsObj = BeautifulSoup(html, 'html.parser')
        #     # loadButton = bsObj.find('smc',{'style':re.compile('none')})
        #     # if loadButton is None:
        #     #     self.driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()
        #     imgs = bsObj.findAll('img',{'alt':re.compile(self._keyword)})
        #     #imgs = bsObj.findAll('img',{'class':'rg_ic'})
        #     for img in imgs:
        #         with open('output.html', 'a', encoding='utf-8') as file:
        #             file.writelines(str(img))












if __name__ == '__main__':
    app = ScrapImgs("엄지",'./')
    app.run()