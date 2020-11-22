import logging
import os
import time

import redis

# prep service
from core.helpers import create_google_credentials

create_google_credentials()

from bot.autoreply import check_mentions
from bot.config import create_api


logger = logging.getLogger()
r = redis.Redis.from_url(os.getenv('REDIS_URL'))

DEFAULT_SLEEP = int(os.getenv("SLEEP_TIME", "10"))


if __name__ == "__main__":

    api = create_api()

    since_id = r.get('since_id')

    if since_id:
        logger.info("Successfully retrieved last tweet id from redis. ID is: {}".format(since_id))
        since_id = int(since_id)
    else:
        since_id = 1
        logger.info("Failed to retriev last tweet id from redis. Defaulting to: {}".format(since_id))
    
    
    while True:
        try:
            since_id, successful = check_mentions(api, since_id)

            if successful:
                logger.info("Updating redis last id ... {}".format(since_id))
                r.set('since_id', since_id)
                logger.info("Successfully updated redis last id")
            
            logger.info("Sleeping ...")
            time.sleep(DEFAULT_SLEEP)
        
        except Exception as e:
            logger.error("Something went wrong! {}".format(e))
