import requests
import gensim
from gensim.summarization import summarize


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

    # words = [word for word in words if word != '\n']

    return ''.join(words)


def create_summary(text: str) -> str:
    summary = summarize(text, word_count = 100)
    return summary


# print(create_summary(parse_content("https://www.youtube.com/api/timedtext?v=r7SO-Oq3d5E&asr_langs=de%2Cen%2Ces%2Cfr%2Cit%2Cja%2Cko%2Cnl%2Cpt%2Cru&caps=asr&exp=xftt&xorp=true&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1612037895&sparams=ip%2Cipbits%2Cexpire%2Cv%2Casr_langs%2Ccaps%2Cexp%2Cxorp%2Cxoaf&signature=0ECE75427BEBB24153B0F31ECD1C5701ABE1D85E.960356CCC5FAAF81621740FCBDC6AD46CF78A693&key=yt8&kind=asr&lang=en&fmt=json3&xorb=2&xobt=3&xovt=3")))

###### OPTIONAL (TIME PERMITTING) #####
# Name entity recognition tags
def ner_tags():
    pass

#
