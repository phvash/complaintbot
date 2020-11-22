import logging

from common.errors import SentimentAnalysisError
from core.dao import Dao, DEFAULT_AGENCIES
from core.sentimentAnalysis import analyze_entity_sentiment
from core.helpers import group_entities_by_sentiment
from core.templates import load_default_templates


logger = logging.getLogger()
dao = Dao()
templates = load_default_templates()


class TweetHandler:

    def handle_tweet(self, tweet, context):
        # check if tweet has been previously handled. 
        # reply with a link to previous response

        # analyse entity sentiments
        try:
            tweet_content = context + ' ' + tweet.text if context else tweet.text
            entities = analyze_entity_sentiment(tweet_content)
            print([e.name.upper() for e in entities])
            neg_entities, neu_entities, pos_entities = group_entities_by_sentiment(entities)

            locale = self.get_location(tweet)
            # we'd only handle negative comments for now
            agencies = self.agencies_from_entities(entities, locale)

            if agencies:
                return self.make_response(agencies)

            logger.info("Unable to match any entity in tweet to agency!")

            # try manual parsing
            agencies = self.agencies_from_text(tweet_content, locale)
            logger.info(f"manually parsing returned: {agencies}")
            if agencies:
                return self.make_response(agencies)

            # default response
            return templates['DEFAULT']


        except SentimentAnalysisError as e:
            logger.error("Sentiment Analysis Failed!. Switching resolving to manual parsing.")

    def extract_entities():
        """ 
        Manually to  extract entities from text
        if automatic fails
        """
        pass

    @staticmethod
    def agencies_from_entities(entities, locale=None):
        agencies = []
        for entity in entities:
            agency = dao.find_agency_by_name(entity.name.upper())
            if agency: # entity matches an agency in our db
                agency.update({'matchedEntity': entity})
                agencies.append(agency)

        # check for default agencies
        if not agencies:
            for entity in entities:
                entity_name = entity.name.upper()
                if entity_name in DEFAULT_AGENCIES:
                    agency = dao.find_default_agency(entity_name, locale)
                    if agency: # entity matches an agency in our db
                        agency.update({'matchedEntity': entity})
                        agencies.append(agency)
        return agencies

    @staticmethod
    def agencies_from_text(text, locale=None):
        agencies = []
        for a in DEFAULT_AGENCIES:
            # print("a: ", a.lower())
            # print("text: ", text.lower())
            if a.lower() in text.lower(): # entity matches an agency in our db
                print(a)
                agency = dao.find_default_agency(a.upper(), locale)
                if agency: # entity matches an agency in our db
                    agency.update({'matchedEntity': a})
                    agencies.append(agency)
        return agencies


    @staticmethod
    def make_response(agencies):
        # interesting case, for now, only response to the entity with most negative 
        response =  templates.get(agencies[0]['uid'])
        if not response:
            response = templates['default']
        return response



    @staticmethod
    def get_location(tweet):
        locale = tweet.user.location
        # default for now
        return "United States of America"
        # return "Nigeria"

