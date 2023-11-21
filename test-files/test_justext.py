import src.python.justext as justext
import requests
page = requests.get('http://planet.python.org/').text.encode('utf-8')

#paragraphs = justext.justext(page, justext.get_stoplist('English'))
paragraphs = justext.justext(page, None)
for paragraph in paragraphs:
    print(paragraph.text)