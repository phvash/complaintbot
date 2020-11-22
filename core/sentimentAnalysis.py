from google.cloud import language_v1



# DEFAULTS

DEFAULT_DOC_TYPE = language_v1.Document.Type.PLAIN_TEXT
DEFAULT_ENCODING_TYPE = language_v1.EncodingType.UTF8
DEFAULT_LANGUAGE = "en"


client = language_v1.LanguageServiceClient()


def analyze_entity_sentiment(text_content):
    """
    Analyzing Entity Sentiment in a String
    Args:
      text_content The text content to analyze
    """
    
    # Cloud NLP supports other languages, but we don't have liberty of time to test those out yet.
    # definitely worth investigating in subsequent releases.

    document = {"content": text_content, "type_": DEFAULT_DOC_TYPE, "language": DEFAULT_LANGUAGE}

    response = client.analyze_entity_sentiment(request = {'document': document, 'encoding_type':DEFAULT_ENCODING_TYPE})

    return response.entities

