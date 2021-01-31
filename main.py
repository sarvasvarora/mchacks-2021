import requests
import os
import json
import gensim
from gensim.summarization import summarize
from flask import escape
from google.cloud import language_v1


def parse_content(captions_url: str) -> str:
    """Parse the JSON from the captions URL and return the text.

    Args:
        captions_url (str): URL of the captions file from YouTube

    Returns:
        str: Text content of the captions
    """
    data = requests.get(f"{captions_url}&fmt=json3").json()

    # create a string of all the words in utf format.
    events = data['events']
    words = []

    for event in events: 
        segments = event['segs'] if 'segs' in event.keys() else None
        if segments is not None:
            for segment in segments:
                words.append(segment['utf8'])
            
    
    words = [word for word in words if word != '\n']

    return ''.join(words)


def create_summary(text: str) -> str:
    """Create a summary out of the input text.

    Args:
        text (str): The input text

    Returns:
        str: 100 word summary of the input text
    """
    summary = summarize(text, word_count = 100)
    return summary




path = "./McHacks-5783c73596b5.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path

def get_top_keywords(content: str):
    """Get the top 5 frequently occuring keywords in the input text

    Args:
        content (str): The input text

    Returns:
        list: List of top 5 keywords
    """

    client = language_v1.LanguageServiceClient()
    type_ = language_v1.Document.Type.PLAIN_TEXT
    language = "en"

    document = {"content": content, "type_": type_, "language": language}
    encoding_type = language_v1.EncodingType.UTF8
    response = client.analyze_entities(request = {'document': document, 'encoding_type': encoding_type})

    number_of_keyword = 0
    keywords = []

    for entity in response.entities:
            print(u"Representative name for the entity: {}".format(entity.name))
            keyword = str(entity.name).strip('.\n ')

            if keyword not in keywords and len(keyword.split()) < 4:
                keywords.append(keyword)
                number_of_keyword +=1

            if number_of_keyword == 5:
                break

    return keywords



def get_summary(request):
    """The main API function, deployed on Google Cloud Function.

    Returns a JSON containing the summary and the top 5 keywords in the text transcript.

    Args:
        request (dict): JSON input containing the URL of the captions file. Format: {"url" : <INSERT URL HERE>}

    Returns:
        dict: JSON dump (string) containing the summary and the list of top 5 keywords
    """
    URL = request.get_json(silent=True)['url']
    text = parse_content(URL)
    text_with_punctuation = requests.post("http://bark.phon.ioc.ee/punctuator", {"text": text})
    text = text_with_punctuation.content.decode('utf-8')

    summary = create_summary(text)
    keywords = get_top_keywords(text)
    
    return json.dumps({"summary" : summary, "keywords" : keywords})