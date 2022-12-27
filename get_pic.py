from bs4 import BeautifulSoup
import requests
from os import path
siteUrl = 'https://www.adidas.com.tr/tr/run-falcon-2.0-tr-ayakkabi/GW4051.html'

headers = {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00 Opera/9.60 (Windows NT 6.0; U; en) Presto/2.1.1'}
def getURL(siteUrl):
    response = requests.get(siteUrl, headers=headers)
    parser = BeautifulSoup(response.text, 'html.parser')
    # htmlfile = open('zara.txt','wb')
    # htmlfile.write(response.content)
    # htmlfile.close()
    return parser

def getImage(imageSourceUrl,imageName):
    imageFileName = '%s.png' % imageName
    image = requests.get(imageSourceUrl,headers=headers)
    imageFile = open(imageFileName, 'wb')
    imageFile.write(image.content)
    imageFile.close()
    return image



parser = getURL(siteUrl)
div = parser.find_all('div',attrs={'class': 'content___3m-ue'})
all_ = [x.find('img') for x in div]
print(all_)
elements = [x['srcset'] for x in all_]
for i in range(len(elements)):
    getImage(elements[i].split()[-2],i)
