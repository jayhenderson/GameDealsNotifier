import praw
import time
from emailer import createServer, createEmailString, sendEmail


MIN_SCORE = 10  # the default minimum score


# TODO: User settings, move to a different file!
targetSubreddit = "gamedeals"
whitelist = ["free", "100", ]
blacklist = ["shipping", "region", "buy", "xbox", "psn", "drm", "weekend", ]


def createUserAgent():
    user_agent = praw.Reddit(user_agent='Game Deal Notifier 1.0')
    return user_agent


def getSubmissions(client, target):
    submissions = client.get_subreddit(target).get_new(limit=25)
    # Or use one of these functions:
    #                                       .get_new
    #                                       .get_hot(limit=25)
    #                                       .get_top_from_year(limit=25)
    #                                       .get_top_from_month(limit=25)
    #                                       .get_top_from_week(limit=25)
    #                                       .get_top_from_day(limit=25)
    #                                       .get_top_from_hour(limit=25)
    #                                       .get_top_from_all(limit=25)
    return submissions


def isValidSubmission(submission):
    title = submission.title.lower()
    return findMatch(title, whitelist, blacklist) and submission.score > MIN_SCORE


def findMatch(title, whitelist, blacklist):
    if not whitelist or any(word in title for word in whitelist):
        if not blacklist or not any(word in title for word in blacklist):
            return True
    return False


def sendNotification(post):
    server = createServer()
    emailString = createEmailString(post[0], post[1])
    sendEmail(server, emailString)


def main():
    reddit = createUserAgent()
    sent = []
    while True:
        notificationQueue = []
        submissions = getSubmissions(reddit, targetSubreddit)
        print("Searching...")
        for submission in submissions:
            if isValidSubmission(submission) and submission.id not in sent:
                notificationQueue.append((submission.title, submission.url))
                sent.append(submission.id)
        for post in notificationQueue:
            try:
                sendNotification(post)
                print("Notification Sent!")
            except:
                continue
        print("Waiting...")
        time.sleep(30)


if __name__ == "__main__":
    main()
