import random
from captureReddit import RedditBot
from VideoFormat import VideoFormat


# Find stuff like website and stuff
def main():

    # Pick a random sub
    sub = random.choice(['first', 'second', 'third', 'fourth'])

    # Webscrape
    reddit = RedditBot()
    titles, commentTitle = reddit.getPost('AskReddit', 5)

    videoFormatList = []
    for i in range(len(titles)):
        videoFormatList.append(VideoFormat(titles[i], commentTitle[i], i))

    print("Videos have been generated")


main()

