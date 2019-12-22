import requests
import bs4
import json
res = requests.get('https://edition.cnn.com/politics')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')


tags = soup.find_all('script')
for tag in tags:
    if 'var CNN = CNN ||' in tag.text:
        jsonStr = tag.text
        jsonStr = jsonStr.split('siblings:')[-1].strip()
        jsonStr = jsonStr.split(']',1)[0] + ']}'
        jsonData = json.loads(jsonStr)

for article in jsonData['articleList']:
    headline = article['headline']
    link = 'https://edition.cnn.com' + article['uri']

    print ('Headline: %s\nLink: %s\n\n' %(headline, link))
