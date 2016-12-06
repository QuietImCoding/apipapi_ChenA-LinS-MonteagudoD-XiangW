import requests, pprint
from flask import Flask

app = Flask(__name__)

@app.route("/")
def randomImages():
    headers = {'Content-type':'application/json', 'api_key':'40dc55834c419934220050a79fd0655dbb1f88083bc729ad9'}

    response = requests.get("http://api.wordnik.com/api/words.json/randomWord", headers)

    word = response.json()['word']
    
    response = requests.get("http://api.wordnik.com/api/word.json/" + word + "/topExample", headers)

    example = response.json()['text']
    
    flickrhead = {}
    flickrhead['api_key'] = '8746e5a7e804588f2c14eee32778068b'
    flickrhead['safe_search'] = '1'
    flickrhead['method'] = 'flickr.photos.search'
    flickrhead['tags'] = word
    flickrhead['format'] = 'json'
    flickrhead['nojsoncallback'] = '1'
    
    response = requests.get("https://api.flickr.com/services/rest/", flickrhead)
    
    photos = []
    for photo in response.json()['photos']['photo']:
        photos.append([photo['farm'], photo['server'], photo['id'], photo['secret']])
        
    urls = []
    for photo in photos:
        urls.append("https://farm%s.staticflickr.com/%s/%s_%s.jpg" % (photo[0], photo[1], photo[2], photo[3]))

    page = ""
    for photo in urls:
        page += "<img src='%s'/>" % photo

    return page

if __name__ == "__main__":
    app.run()

