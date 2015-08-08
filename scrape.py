#!/usr/bin/env python
import praw
from twilio.rest import TwilioRestClient
from settings import ACCOUNT_SID, AUTH_TOKEN, SUBSCRIBERS


client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

def main():
    r = praw.Reddit(user_agent='shower_texts')
    submissions = r.get_subreddit('showerthoughts').get_top(limit=2)
    #  params = {'t': 'all'}
    submission = submissions.next()
    submission = submissions.next()
    for number in SUBSCRIBERS:
        client.messages.create(
            to=number,
            from_="+14152002895",
            body=submission.title,
        )

if __name__ == '__main__':
    main()
