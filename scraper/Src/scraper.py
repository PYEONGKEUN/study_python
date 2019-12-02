
# -*- coding: utf-8 -*- 
# selenium module
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import threading 

# mobile_emulation = {

#     "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },

#     "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }

# chrome_options = Options()

# chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
# bs4 module
import re
from bs4 import BeautifulSoup
import time
# convert base64 to img
import base64
#down images
import urllib.request

# file IO lib
import os
import sys
import traceback
import logging as LOGGER


class StopException(Exception):
    def __init__(self):
        super().__init__('키워드를 확인하세요')


LOGGER.basicConfig(filename='./log.txt', level=LOGGER.DEBUG)
class ScrapImgs:


    def __init__ (self, savePath, fileName,all_these_words= '',this_exact_word_or_phrase= '',any_of_these_words= '',none_of_these_words= ''):
        self._savePath = os.path.abspath(savePath)
        self._fileName = fileName        
        self._all_these_words = all_these_words
        self._this_exact_word_or_phrase = this_exact_word_or_phrase
        self._any_of_these_words = any_of_these_words
        self._none_of_these_words = none_of_these_words
        self._SLEEP_TIME = 1
        self._SCROLL_SLEEP_TIME = 1
        self._SCROLL_SIZE = 1080
        self.driver = webdriver.Chrome('.\chromedriver.exe')
        self._progress = 0.0
        self._lockProgress= threading.Lock()
        self._fileNum = self.initFileNum()
        #self._lockFileNum = threading.Lock()
        self._totalDownThreadCnt = 20
        self._lockTotalDownThreadCnt = threading.Lock()        
        self._curDownThreadCnt = 0
        self._lockCurDownThreadCnt = threading.Lock()
        self._stepSize = 0

        #self.driver = webdriver.Chrome(chrome_options = chrome_options)

    # 저장하려는 이름을 가진 파일이 존재한다면 다른 이름으로 바꿈 -> 이름뒤에 붙는 숫자를 변경
    def initFileNum(self):
        num = 0
        namePattern = re.compile(self._fileName+'_'+'\d+')
        numPattern = re.compile('\d+')
        filenames = os.listdir(self._savePath)
        for filename in filenames:
            if re.match(namePattern, filename):
                splitFilename = re.split('[._]', filename)                
                if re.match(numPattern, splitFilename[1]):
                    if int(splitFilename[1]) > num:
                        num = int(splitFilename[1])
       
        return num

    

    def teardown_method(self, method):
        self.driver.quit()

    def increasePregress(self, flt):
        if self._progress < 100.0 :
            self._progress += flt
        else:
            pass

    def downImgBase64(self,img, fileNum):
        self._lockCurDownThreadCnt.acquire()
        self._curDownThreadCnt +=1
        self._lockCurDownThreadCnt.release()
               
        path = os.path.join(self._savePath,self._fileName+'_'+str(fileNum)+'.jpg')        
        with open(path, 'wb') as file:
            file.write(base64.b64decode(str(img['src']).split(',')[1]))        
        
        
        #Shared Data만 감싸준다
        





        self._lockProgress.acquire()
        self.increasePregress(self._stepSize)
        print('##progress : '+'{:04.2f}%' .format(self._progress))   
        self._lockProgress.release() 

        self._lockCurDownThreadCnt.acquire()
        self._curDownThreadCnt -=1
        self._lockCurDownThreadCnt.release()

        
        

    def DownImgUrl(self,img, fileNum):
        self._lockCurDownThreadCnt.acquire()
        self._curDownThreadCnt +=1
        self._lockCurDownThreadCnt.release()
               
        path = os.path.join(self._savePath,self._fileName+'_'+str(fileNum)+'.jpg')        
        urllib.request.urlretrieve(str(img['src']),path)        
        
        #Shared Data만 감싸준다        




        self._lockProgress.acquire()
        self.increasePregress(self._stepSize)
        print('##progress : '+'{:04.2f}%' .format(self._progress))   
        self._lockProgress.release()

        self._lockCurDownThreadCnt.acquire()
        self._curDownThreadCnt -=1
        self._lockCurDownThreadCnt.release()             

        
        

    def run(self):
        try:
            LOGGER.info('selenium Chrome Driver Loaded')
            LOGGER.info('waiting 3 seconds....')
            self.driver.implicitly_wait(self._SLEEP_TIME)




            #구글 이미지 검색에 접근      
            self.driver.get('https://www.google.co.kr/imghp?hl=ko')
            #self.driver = driver.Remote('https://www.google.co.kr/imghp?hl=ko',desired_caps)
            
            time.sleep(self._SLEEP_TIME)
            self.driver.set_window_size(1021, 1000)
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

            
            # html = self.driver.page_source


            # Beautiful Soup 으로 이미지 소스 파싱
            # bsObj = BeautifulSoup(html, 'html.parser')
            # isKeywordChanged = bsObj.findAll('div',text=re.compile('대신 검색'))
            # if isKeywordChanged is not None:
            #     print('검색어가 잘못 되었습니다 확인하고 다시 입력하세요.')
            #     raise StopException


            
            #검색 결과에서 스크롤 -> 사람이 하는것처럼 딜레이를 주어 구글을 속임
            prevPageYOffset = self.driver.execute_script('return window.pageYOffset;')
            blockTime = 0
            for i in range(1,10000):
                self.driver.execute_script("window.scrollTo(0,"+str(i*self._SCROLL_SIZE)+")")
                if(prevPageYOffset == self.driver.execute_script('return window.pageYOffset;')):
                    if(blockTime == 2) : break
                    html = self.driver.page_source
                    bsObj = BeautifulSoup(html, 'html.parser')
                
                    # 검색결과 더보기 버튼은 항상 존재하지만 
                    # style="display:none" style="" 로 보였다 안보였다 한다
                    

                    showMore = bsObj.find_all('input',{'value':'결과 더보기'})
                    showMoreIsDisplay = bsObj.find_all({'id':'smc','style':re.compile('none')})
                    

    

                    #스크롤이 더이상 내려가지 않고 결과 더보기 버튼이 생겼을때 버튼을 클릭하는 부분
                    if(showMore is not None ):
                        for element in showMore:
                            xpath = "//input["
                            #print(element.attrs)
                            for idx, (key, val) in enumerate(element.attrs.items()):
                                if key != 'class':
                                    if(idx != len(element.attrs)-1):                            
                                        xpath+= '@'+str(key)+'="'+val+'" and '
                                    else:
                                        xpath+= '@'+str(key)+'="'+str(val)+'"]'
                            #print(xpath)
                            #self.driver.find_element_by_css_selector("input[class='ksb'][value='결과 더보기']").clcik()
                            #print(self.driver.find_element_by_xpath(xpath))
                            # try:
                                
                            #     self.driver.find_element_by_xpath(xpath).clcik()
                            # except Exception as e:
                            #     print(e)
                            try:
                                self.driver.find_element_by_xpath(xpath).send_keys(Keys.ENTER)
                            except Exception as e:
                                print(e)
                    else:
                        noImages = bsObj.findAll('div',text='더 이상 표시할 콘텐츠가 없습니다.')
                        if(noImages is not None): break
                    blockTime +=1

                time.sleep(self._SCROLL_SLEEP_TIME)
                prevPageYOffset = self.driver.execute_script('return window.pageYOffset;')
                
            # 이미지 소스를 가져올 페이지 복사후 selenium 크롬 종료
            html = self.driver.page_source
            self.driver.quit()

            # Beautiful Soup 으로 이미지 소스 파싱
            bsObj = BeautifulSoup(html, 'html.parser')
            imgsBase64 = bsObj.findAll('img',{'alt':re.compile('이미지'),'src':re.compile('base64')})
            imgsUrl = bsObj.findAll('img',{'alt':re.compile('이미지'),'src':re.compile('http')})
            #imgsBase64 = bsObj.findAll('img',{'src':re.compile('base64')})
            #imgsUrl = bsObj.findAll('img',{'src':re.compile('http')})
            


            # html에 img 태그들 수집
            for img in imgsBase64:
                with open(self._fileName+'.html', 'a', encoding='utf-8') as file:
                    file.writelines(str(img))
            for img in imgsUrl:
                with open(self._fileName+'.html', 'a', encoding='utf-8') as file:
                    file.writelines(str(img))
            
            #다운해야할 파일 갯수 계산 & process increase 값 설정
            totalCnt = len(imgsBase64) + len(imgsUrl)
            print("총 "+str(totalCnt)+"개의 사진을 찾았습니다!")
            self._stepSize = 100.0 / totalCnt
            


            if(True):
                #멀티스레딩을 사용한 이미지 다운로드
                idxImgsBase64 = 0 
                
                while(True):
                    if(len(imgsBase64) == 0 or idxImgsBase64 > len(imgsBase64)-1 ): break
                    if(self._curDownThreadCnt < self._totalDownThreadCnt ):
                        self._fileNum +=1
                        arg = imgsBase64[idxImgsBase64]
                        th = threading.Thread(target=self.downImgBase64, args=[arg,self._fileNum])
                        th.start()               
                        idxImgsBase64+=1
                    #time.sleep(0.05)
                idxImgsUrl = 0 
                
                while(True):
                    
                    if(len(imgsUrl) == 0 or idxImgsUrl > len(imgsUrl)-1): break

                    if(self._curDownThreadCnt< self._totalDownThreadCnt ):
                        self._fileNum +=1
                        arg = imgsUrl[idxImgsUrl]
                        th = threading.Thread(target=self.DownImgUrl, args=[arg,self._fileNum])
                        th.start()                
                        idxImgsUrl+=1
                    #time.sleep(0.05)
            else:
                            

            
            #멀티스레딩을 사용하지 않은 이미지 다운로드
            

                for img in imgsBase64:
                    path = os.path.join(self._savePath,self._fileName+'_'+str(self._fileNum)+'.jpg') 
                    with open(path, 'wb') as file:
                        file.write(base64.b64decode(str(img['src']).split(',')[1]))
                    self._fileNum+=1
                    self.increasePregress(self._stepSize)
                    print('##progress : '+'{:04.2f}%' .format(self._progress))
                
                

                for img in imgsUrl:
                    path = os.path.join(self._savePath,self._fileName+'_'+str(self._fileNum)+'.jpg') 
                    urllib.request.urlretrieve(str(img['src']),path)
                    self._fileNum+=1
                    self.increasePregress(self._stepSize)
                    print('##progress : '+'{:04.2f}%' .format(self._progress))

        except StopException:
            None
        













if __name__ == '__main__':
    start = time.time()
    #파일 저장 경로
    arg1 = './'
    #저장할 이미지 이름 ex(올라프 -> 올라프_0 ~ 올라프_12)
    arg2 = '올라프'
    #다음 단어 모두 포함
    arg3 = '올라프'
    #다음 단어 또는 문구 정확하게 포함
    arg4 = '겨울왕국 아트 그림'
    #다음 단어 중 아무거나 포함
    arg5 = ''
    #다음 단어 제외
    arg6 = '감독 배우 유아'

    app = ScrapImgs(arg1,arg2,arg3,arg4,arg5,arg6)
    app.run()

    while(True):
        if (app._curDownThreadCnt == 0):
            print("time :", time.time() - start)
            break