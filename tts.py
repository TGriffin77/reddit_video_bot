from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time
import os


def grab_speech(text, iteration):
    dir = '.\\results'
    op = Options()
    prefs = {'download.default_directory': dir}
    op.add_experimental_option('prefs', prefs)

    s = Service("C:\\Program Files (x86)\\chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=op)
    driver.get('https://ttstool.com/')

    time.sleep(1)

    selectEnglish = driver.find_element(By.XPATH, '//option[@value="English"]')
    selectEnglish.click()

    time.sleep(0.5)

    selectBrian = driver.find_element(By.XPATH, '//option[@value="3"]')
    selectBrian.click()

    textArea = driver.find_element(By.XPATH, '//textarea[@rows="4"]')
    textArea.send_keys(text)

    downloadButton = driver.find_elements(By.XPATH, '//i[@class="material-icons button"]')
    downloadButton[1].click()
    time.sleep(5)
    os.rename(dir+'\\narration.mp3' , dir+f'\\voice{iteration}.mp3')

    driver.close()
    return dir+f'\\voice{iteration}.mp3'


def determineLengths(text):
    length = 0
    textQueues = [0]
    for i in text:
        if i == ',' or i == ':':
            length+=0.318
            textQueues.append(length)
        elif i == '.' or i == '!' or i == '?':
            length+=0.600
            textQueues.append(length)
        elif i == ' ':
            length+=0.035
        else:
            length+=0.080
    textQueues.append(length)
    return length, textQueues


x = 'hello: how are you today. That is so nice to hear'
determineLengths(x)
#grab_speech(x,0)