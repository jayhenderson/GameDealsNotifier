import praw
import time
from emailer import create_server, create_email_string, send_email

MIN_SCORE = 10  # the default minimum score

# TODO: User settings, move to a different file!
TARGET_SUBREDDIT = "gamedeals"
WHITELIST = ["free", "100", ]
BLACKLIST = ["shipping", "region", "buy", "xbox", "psn", "drm", "weekend", ]


def create_user_agent():
    user_agent = praw.Reddit(user_agent='Game Deal Notifier 1.0')
    return user_agent


def get_submissions(client, target):
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


def is_valid_submission(submission):
    title = submission.title.lower()
    return find_match(title) and submission.score > MIN_SCORE


def find_match(title):
    if not WHITELIST or any(word in title for word in WHITELIST):
        if not BLACKLIST or not any(word in title for word in BLACKLIST):
            return True
    return False


def send_notification(post):
    server = create_server()
    email_string = create_email_string(post[0], post[1])
    send_email(server, email_string)


def main():
    reddit = create_user_agent()
    sent_notifications = []
    while True:
        notification_queue = []
        submissions = get_submissions(reddit, TARGET_SUBREDDIT)
        print("Searching...")
        for submission in submissions:
            if is_valid_submission(submission) and submission.id not in sent_notifications:
                notification_queue.append((submission.title, submission.url))
                sent_notifications.append(submission.id)
        for post in notification_queue:
            try:
                send_notification(post)
                print("Notification Sent!")
            except:
                continue
        print("Waiting...")
        time.sleep(30)


if __name__ == "__main__":
    main()
