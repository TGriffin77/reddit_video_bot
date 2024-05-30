import os
import random
import time
import numpy as np

from PIL import Image, ImageFont, ImageDraw
import textwrap

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import wave
from pydub import AudioSegment

import moviepy.editor as mp


class VideoFormat:

    bad_words = [] #add a list of words to filter
    censored_words = {} # dictionary: key = bad word, value = replace with this word

    def __init__(self, titleList, commentList, iteration):
        self.title = titleList[0]
        self.approved = self.verifyTitle()
        if self.approved:
            self.iteration = iteration
            self.cleanTitle()
            self.author = titleList[1]
            self.upvotes = titleList[2]
            self.commentCount = titleList[3]
            self.commentList = self.cleanComment(self.verifyComment(commentList))
            self.titleImage = self.createTitleImage()
            self.compiledText, self.commentList = self.compileComments() #Need to generate textwrap for commentList
            self.audio = self.generateAudio()
            self.audioQueues = self.determineAudioQueues()
            print(self.audioQueues)
            self.commentImages = self.createCommentImage()
            self.generateVideo()


    def verifyTitle(self):
        temp = self.title.lower()
        return not (len(temp) >= 121 or any(word in temp for word in self.bad_words))


    def cleanTitle(self):
        temp = self.title.lower()
        for word in self.censored_words:
            if temp.__contains__(word):
                temp = temp.replace(word, self.censored_words[word])

        self.title = temp.capitalize()


    def verifyComment(self, comList):
        tempList = []
        tempComment = list(comList)
        for comment in tempComment:
            comment = comment.lower()
            if comment.__contains__('edit'):
                editIndex = comment.find('edit')
                temp = comment[editIndex + 4]
                if any(x == temp for x in ['-',':','\n']):
                    comment = comment[:editIndex]
            if not (len(comment) < 70 or len(comment) > 600) or any(word in comment for word in self.bad_words):
                tempList.append(comment.capitalize())
        return tempList


    def cleanComment(self, comList):
        tempList = []
        tempComment = list(comList)
        for comment in tempComment:
            temp = comment.lower()
            for word in self.censored_words:
                if temp.__contains__(word):
                    temp = comment.replace(word, self.censored_words[word])
            tempList.append(temp.capitalize())

        return tempList


    def createTitleImage(self):
        def reformat_num(number):
            temp = ''
            if number // 1000 != 0:
                temp += str(number // 1000)
                temp += '.'
                temp += str((number % 1000) // 100)
                temp += 'k'
                return temp

        backplate = Image.open(".\\sources\\Title.jpg")

        title_font = ImageFont.truetype('.\\sources\\title_font.ttf', size=100)  # rgb(215, 218, 220)
        author_font = ImageFont.truetype('.\\sources\\submission_font.ttf', size=76)  # rgb(129, 131, 132)
        upvote_font = ImageFont.truetype('.\\sources\\upvote_font.ttf', size=76)  # rgb(215, 218, 220)
        comment_font = ImageFont.truetype('.\\sources\\upvote_font.ttf', size=76)  # rgb(129, 131, 132)

        backplate_editable = ImageDraw.Draw(backplate)

        title = textwrap.fill(text=self.title, width=26)
        author = f"Submitted by u/{self.author} {random.randint(2, 23)} hours ago"
        upvote = reformat_num(self.upvotes)
        comment = reformat_num(self.commentCount)
        comment = f"{comment} Comments"

        backplate_editable.text((280, 130), title, (215, 218, 220), font=title_font)
        backplate_editable.text((15, 15), author, (129, 131, 132), font=author_font)
        backplate_editable.text((20, 400), upvote, (215, 218, 220), font=upvote_font)
        backplate_editable.text((15, 800), comment, (129, 131, 132), font=comment_font)

        saveDir = f'.\\results\\title{self.iteration}.jpg'
        backplate.save(saveDir)
        return saveDir


    def createCommentImage(self):
        os.mkdir(f'.\\results\\imageset{self.iteration}')


        comment_font = ImageFont.truetype('.\\sources\\comment_font.ttf', size=14) # (215,218,220)
        upvote_font = ImageFont.truetype('.\\sources\\submission_font.ttf', size=16) # (215,218,220)
        hour_ago_font = ImageFont.truetype('.\\sources\\comment_font.ttf', size=12) # (72, 73, 74)


        commentImages = []
        for i in range(len(self.commentList)):
            if i != 0:
                hour_ago = random.randint(2, 24)
                upvote_count = random.randint(1,9)
                redditUser = random.choice(['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink']) + '.jpg'
                x = 595
                y = 90
                amountOfLines = 0
                for letter in self.commentList[i]:
                    if letter == '\n':
                        y += 21
                        amountOfLines +=1

                temp = self.commentList[i][:-1]
                temp = temp.replace('.', ',')
                temp = temp.replace('?', ',')
                temp = temp.replace('!', ',')
                temp = temp.replace(':', ',')
                temp = temp.replace('-', ',')
                temp = temp.split(',')
                for j in range(len(temp)):
                    image = Image.new(mode = 'RGBA', size=(x,y), color=(25, 25, 26, 255))

                    redditUserImage = Image.open(f'redditUsers/{redditUser}')
                    redditUserImage.resize((36,36))

                    image.paste(redditUserImage, (8,4))
                    image.paste(Image.open('sources/upvote.png'), (64, 58+ amountOfLines*21))
                    image.paste(Image.open('sources/downvote.png'), (124, 58+ amountOfLines*21))
                    image.paste(Image.open('sources/other.png'), (150, 55 + amountOfLines*21))

                    imageDraw = ImageDraw.Draw(image)
                    s = ''
                    for k in range(j + 1):
                        s += temp[k] + '. '
                    #pfp =

                    imageDraw.text((165,13), str(hour_ago)+' hr. ago', (72, 73, 74), font=hour_ago_font)
                    imageDraw.text((66,36), s, (215,218,220), font=comment_font)
                    imageDraw.text((90,58 + amountOfLines*21), str(upvote_count) +'.5k', (215, 218, 220), font=upvote_font)

                    imageDir = f'.\\results\\imageset{self.iteration}\\image{i}-{j}.png'
                    commentImages.append(imageDir)
                    image.save(imageDir)
        return commentImages


    def compileComments(self):
        confirmedText = [self.title]
        s = self.title
        i = 0
        # Title + comments (characters range 450 - 600)
        while len(s) < 450 or i < len(self.commentList):
            comment = self.commentList[i]
            if len(s) + len(comment) < 600:
                s += comment
                confirmedText.append(comment)
            i+=1

        # Add a period to the end of all comments, if needed.
        sWithPeriods = ''
        for i in range(len(confirmedText)):
            temp = confirmedText[i]
            if temp[-1] == '.' or temp[-1] == '!' or temp[-1] == '?' or temp[-1] == '\n' or temp[-1] == '-':
                temp = confirmedText[i]
            else:
                confirmedText[i] = temp + '.'
                temp += '.'

            sWithPeriods += str('\n' + temp)
        for i in range(len(confirmedText)):
            confirmedText[i] = textwrap.fill(text=confirmedText[i], width=72)
        return sWithPeriods, confirmedText


    def generateAudio(self):
        resultsDir = '.\\results'
        op = Options()
        prefs = {'download.default_directory': resultsDir}
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
        textArea.send_keys(self.compiledText)

        downloadButton = driver.find_elements(By.XPATH, '//i[@class="material-icons button"]')
        downloadButton[1].click()
        time.sleep(5)
        os.rename(resultsDir + '\\narration.mp3', resultsDir + f'\\voice{self.iteration}.mp3')

        driver.close()
        return resultsDir + f'\\voice{self.iteration}.mp3'


    def determineAudioQueues(self):

        wavDir = f'.\\results\\voice{self.iteration}.wav'

        # Convert to wav
        mp3Sound = AudioSegment.from_mp3(self.audio)
        mp3Sound.export(wavDir, format='wav')

        obj = wave.open(wavDir, 'rb')

        sample_freq = obj.getframerate()
        n_samples = obj.getnframes()
        signal_wave = obj.readframes(-1)

        obj.close()

        signal_array = np.frombuffer(signal_wave, dtype=np.int16)

        blankIndices = [0]

        i = 0
        while i < len(signal_array - 1):
            if abs(signal_array[i]) <= 10:
                works = True
                sumAbove = 0
                if (i < len(signal_array - 1) - (.2 * sample_freq)) and (i > (.5*sample_freq)):
                    for j in range(i, i + int(.2 * sample_freq)):
                        if abs(signal_array[j]) > 10:
                            sumAbove += 1
                    if sumAbove < int(sample_freq*.02):
                        blankIndices.append(i)
                        i += int(.5 * sample_freq)
            i += (int(sample_freq * 0.002))

        for index in range(len(blankIndices)):
            blankIndices[index] = blankIndices[index] / sample_freq

        blankIndices.append(n_samples/sample_freq)
        return blankIndices


    def generateVideo(self):
        audioClip = mp.AudioFileClip('sources\\GymnopedieNo1.mp3')
        textAudio = mp.AudioFileClip(self.audio)
        fullAudio = mp.CompositeAudioClip([audioClip, textAudio])
        fullAudio.fps = audioClip.fps
        fullAudio.duration = textAudio.duration + 2

        background = mp.VideoFileClip("sources\\clip.mp4")
        image = (mp.ImageClip(self.titleImage)
                 .resize(width=background.w * .7)
                 .set_duration(self.audioQueues[1]-self.audioQueues[0])
                 .set_position(("center", "center"))
                 )

        allContentList = [background, image]

        for i in range(len(self.commentImages)):

            allContentList.append(mp.ImageClip(self.commentImages[i])
                                  .resize(width=background.w * .7)
                                  .set_start(self.audioQueues[i+1])
                                  .set_end(self.audioQueues[i+2])
                                  .set_position(('center', 'center'))
                                  )

        final = mp.CompositeVideoClip(allContentList)
        final.audio = fullAudio
        final.duration = textAudio.duration + 2
        final.write_videofile(f"finished\\final{self.iteration}.mp4")

