#!/usr/bin/env python
import praw
from twilio.rest import TwilioRestClient
from settings import ACCOUNT_SID, AUTH_TOKEN


client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

def main():
    r = praw.Reddit(user_agent='shower_texts')
    submissions = r.get_subreddit('showerthoughts').get_top(limit=1, params = {'t': 'all'})
    for submission in submissions:
        print submission.title
        client.messages.create(
            to="2096223425",
            from_="+14152002895",
            body=submission.title,
        )

if __name__ == '__main__':
    main()
