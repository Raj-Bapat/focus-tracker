import argparse
import io
import json
import os

from google.cloud import language_v1
import six
import html2text

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/r/Downloads/Classification_Example-39fb93b46092.json"



def classify(text, verbose=True):
    """Classify the input text into categories. """

    language_client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = language_client.classify_text(request={'document': document})
    # print(response)
    categories = response.categories

    result = {}

    for category in categories:
        # Turn the categories into a dictionary of the form:
        # {category.name: category.confidence}, so that they can
        # be treated as a sparse vector.
        result[category.name] = category.confidence

    # if verbose:
    #     # print(text)
    #     for category in categories:
    #         print(u"=" * 20)
    #         print(u"{:<16}: {}".format("category", category.name))
    #         print(u"{:<16}: {}".format("confidence", category.confidence))

    return result


# str = "World of Warships - free-to-play naval warfare-themed massively multiplayer game from Wargaming. Get the latest news and developments here and play for free!"
#
# classify(str)

# worldofwarships.com with all: 75.99
# without: 72.0
# stackoverflow with all: 87.9
# without: stackoverflow without: 50.9
# reddit.com with all: 79.00
# without: 81.9



def getHtmlFromTab():
    ret1 = os.popen("osascript -e \'tell application \"Google Chrome\" to set source to execute front window\'\"\'\"\'s active tab javascript \"document.documentElement.outerHTML\"\'").read().strip()
    h = html2text.HTML2Text()
    h.ignore_links = True
    htstr = h.handle(ret1)
    # print(htstr)
    htstr = ''.join([i if ord(i) < 128 else ' ' for i in htstr])
    htstr = htstr[0:min(1000, len(htstr))]
    return htstr

def predictCategory():
    classify(getHtmlFromTab())



def sample_analyze_sentiment(text_content):
    """
    Analyzing Sentiment in a String

    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()

    # text_content = 'I am so happy and joyful.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    # Get overall sentiment of the input document
    # print(u"Document sentiment score: {}".format(response.document_sentiment.score))
    # print(
    #     u"Document sentiment magnitude: {}".format(
    #         response.document_sentiment.magnitude
    #     )
    # )
    # Get sentiment for all sentences in the document
    # for sentence in response.sentences:
        # print(u"Sentence text: {}".format(sentence.text.content))
        # print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
        # print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    # print(u"Language of the text: {}".format(response.language))

