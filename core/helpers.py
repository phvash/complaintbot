import os
import json
import base64


NEGATIVE_THRESHOLD = float(os.getenv('NEGATIVE_THRESHOLD', '-0.25'))
POSITIVE_THRESHOLD = float(os.getenv('POSITIVE_THRESHOLD', '0.25'))

# analysis helpers
def group_entities_by_sentiment(entities):
    """
    splits entities into 3 groups based on sentitiment value
    returns a tupple of (pos_entities, neg_entities) 
    """

    positive = []
    neutral = []
    negative = []

    for entity in entities:
        sentiment = entity.sentiment
        if sentiment.score <= NEGATIVE_THRESHOLD:
            negative.append(entity)
        elif sentiment.score >= POSITIVE_THRESHOLD:
            positive.append(entity)
        else:
            neutral.append(entity)

    return negative, neutral, positive


def create_google_credentials():
    encoded_data = os.getenv('GOOGLE_AUTH')
    file_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    decoded_data = json.loads(base64.b64decode(encoded_data).decode())
    if not os.path.exists(file_path):
        with open(file_path, 'w') as json_file:
            json.dump(decoded_data, json_file)
            print(f'{file_path} was created in fs')
    else:
        print(f'{file_path} already exists')
