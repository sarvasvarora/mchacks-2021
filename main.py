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
    summary = summarize(text, word_count = 100)
    return summary




path = "key.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path

def get_top_keywords(content):
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

            ##### If we want to display more information about the keywords
            
            # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
            #print(u"Entity type: {}".format(language_v1.Entity.Type(entity.type_).name))

            # Get the salience score associated with the entity in the [0, 1.0] range
            #print(u"Salience score: {}".format(entity.salience))


            #for metadata_name, metadata_value in entity.metadata.items():
                #print(u"{}: {}".format(metadata_name, metadata_value))

            # Loop over the mentions of this entity in the input document.
            # The API currently supports proper noun mentions.
            #for mention in entity.mentions:
                #print(u"Mention text: {}".format(mention.text.content))

            # Get the mention type, e.g. PROPER for proper noun
            #print(u"Mention type: {}".format(language_v1.EntityMention.Type(mention.type_).name))
    return keywords



def get_summary(request):
    headers = {}
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    URL = request.get_json(silent=True, force=True)['url']
    text = parse_content(URL)
    text_with_punctuation = requests.post("http://bark.phon.ioc.ee/punctuator", {"text": text})
    text = text_with_punctuation.content.decode('utf-8')

    summary = create_summary(text)
    keywords = get_top_keywords(text)

    return (json.dumps({"summary" : summary, "keywords" : keywords}), 200, headers)