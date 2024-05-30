from PIL import Image, ImageFont, ImageDraw
import textwrap
import os
import random

def create_image(title, author, upvote, comment):
    def reformat_num(number):
        temp = ''
        if number // 1000 != 0:
            temp += str(number // 1000)
            temp += '.'
            temp += str((number % 1000)//100)
            temp += 'k'
            return temp
    dir = ".\\"
    backplate = Image.open(dir+"sources\\Title.jpg")

    title_font = ImageFont.truetype(dir+'sources\\title_font.ttf', size=100)  # rgb(215, 218, 220)
    author_font = ImageFont.truetype(dir+'sources\\submission_font.ttf', size=76)  # rgb(129, 131, 132)
    upvote_font = ImageFont.truetype(dir+'sources\\upvote_font.ttf', size=76) # rgb(215, 218, 220)
    comment_font = ImageFont.truetype(dir+'sources\\upvote_font.ttf', size=76) # rgb(129, 131, 132)

    backplate_editable = ImageDraw.Draw(backplate)

    upvote = reformat_num(upvote)
    comment = reformat_num(comment)

    title = textwrap.fill(text=title, width=26)
    author = f"Submitted by u/{author} {random.randint(2,23)} hours ago"
    comment = f"{comment} Comments"

    backplate_editable.text((280, 130), title, (215, 218, 220), font=title_font)
    backplate_editable.text((15, 15), author, (129, 131, 132), font=author_font)
    backplate_editable.text((20, 400), upvote, (215, 218, 220), font=upvote_font)
    backplate_editable.text((15, 800), comment, (129, 131, 132), font=comment_font)

    saveDir = dir+'results\\title.jpg'
    backplate.save(saveDir)
    return saveDir
