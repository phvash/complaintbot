import logging

import tweepy
from core.handler import TweetHandler

handler = TweetHandler()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def check_mentions(api, since_id):
    logger.info("Retrieving mentions")
    
    new_since_id = since_id
    successful = False

    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id = since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        context = None

        if tweet.in_reply_to_status_id is not None: # direct mention, not under a reply
            replied_tweet = api.get_status(tweet.in_reply_to_status_id, tweet_mode='extended')._json['full_text']
            context = replied_tweet
        
        logger.info(f"Answering to [{context}] | [{tweet.text}] from {tweet.user.name}")

        response = handler.handle_tweet(tweet, context)

        if response:
            api.update_status(
                status='@' + tweet.user.screen_name + ' ' + response,
                in_reply_to_status_id=tweet.id,
            )
            logger.info("Succesfully replied mention ['{}'] with response ['{}']".format(tweet.text, response))
            successful = True

    return new_since_id, successful
