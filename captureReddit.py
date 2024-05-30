import praw
import random
import os
from dotenv import load_dotenv

class RedditBot:
    def __init__(self):
        load_dotenv()
        self.reddit = praw.Reddit(client_id=os.getenv('CLIENT_ID'),
                                 client_secret=os.getenv('CLIENT_SECRET'),
                                 password=os.getenv('CLIENT_PASSWORD'),
                                 user_agent=os.getenv('CLIENT_USER_AGENT'),
                                 username=os.getenv('CLIENT_USERNAME'))

    def getPost(self, sub, limit):
        subreddit = self.reddit.subreddit(sub)

        top_reddit = subreddit.top(limit=limit, time_filter='week')

        submissionList = []  # list of titles, upvotes, and comments
        titleCommentList = []  # list of comments in each title

        for submission in top_reddit:
            submissionList.append([submission.title,  submission.author.name, submission.ups, random.randint(submission.ups//4.5, submission.ups//1.2)])
            commentList = []

            submission.comments.replace_more(limit=0)
            for comment in submission.comments:
                if len(comment.body) > 50:
                    commentList.append(comment.body)


            titleCommentList.append(commentList)

        return submissionList, titleCommentList

