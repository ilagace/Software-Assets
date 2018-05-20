from bs4 import BeautifulSoup
import urllib2, os, datetime
import csv

with open('listgo', 'rb') as f:
    reader = csv.reader(f)
    go_comics_pages = list(reader)
with open('listoregon', 'rb') as f:
    reader = csv.reader(f)
    go_oregon_pages = list(reader)

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

creator_pages = ["http://www.arcamax.com/thefunnies/archie/"]
crankshaft_page = ["https://www.arcamax.com/thefunnies/crankshaft/"]

images = {}
today = datetime.datetime.today().strftime("/%Y-%m-%d")

def go_comic(pages):
    for url in pages:
        print(url[1])
        req = urllib2.Request(url[1], headers=hdr)

        try:
            content = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.fp.read()

        soup = BeautifulSoup(content,"html.parser")

        for link in soup.find_all('picture'):
            #print(link.get('class'))
            if link.get('class') == [u'gc-card__image', u'gc-card__image--cropped-strip', u'lazyload__padder', u'lazyload__padder--card']:
                print(link.next_element.get('src'))
                filename = url[1][url[1].find(".com/")+5:]
                images[filename] = [link.next_element.get('src'),url[0]]
                break
    return images

def go_creator(pages):
    for url in pages:
        req = urllib2.Request(url, headers=hdr)

        try:
            content = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.fp.read()

        soup = BeautifulSoup(content,"html.parser")

        for link in soup.find_all('img'):
            #print(link)
            if link.get('src').find("/newspics/") >= 0:
                filename = "archie"
                images[filename] = ["http://www.arcamax.com" + link.get('src'),'archie']

    return images

def go_crankshaft(pages):
    for url in pages:
        req = urllib2.Request(url, headers=hdr)

        try:
            content = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.fp.read()

        soup = BeautifulSoup(content,"html.parser")

        for link in soup.find_all('img'):
            #print(link)
            if link.get('src').find("/newspics/") >= 0:
                filename = "crankshaft"
                images[filename] = ["http://www.arcamax.com" + link.get('src'),'49']

    return images

def go_oregon(pages):
    for url in pages:
        urld = url[1] + today
        print(urld)
        req = urllib2.Request(urld, headers=hdr)

        try:
            content = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print(e,url)

        soup = BeautifulSoup(content,"html.parser")
        for links in soup.find_all('img'):
            if links.get('src').find("safr.kingfeatures.com") >= 0:
                print('found')
                filename = url[1][url[1].find(".com/")+5:]
                images[filename] = [links.get('src'),url[0]]

    return images

#Mr. Boffo section
url = "http://www.mrboffo.com"
print(url)
req = urllib2.Request(url, headers=hdr)

try:
    content = urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.fp.read()

else:
    soup = BeautifulSoup(content,"html.parser")
    for link in soup.find_all('img'):
        if link.get('src').find(".com/images/daily") >= 0:
            filename = "mrboffo"
            images[filename] = [link.get('src'),'mrboffo']

#Dilbert section
url = "http://www.dilbert.com"
print(url)
req = urllib2.Request(url, headers=hdr)

try:
     content = urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.fp.read()

except urllib2.HTTPError, e:
    print(e.fp.read())
else:
    soup = BeautifulSoup(content,"html.parser")
    for link in soup.find_all('img'):
        if link.get('src').find("assets.amuniver") >= 0:
            filename = "dilbert"
            images[filename] = [link.get('src'),'dilbert']
            break

def from_url( url, filename):
    '''Store the url content to filename'''

    if url.find("content-error-missing-image") >= 0:
        return False
    req = urllib2.Request( url, headers=hdr )
    try:
        response = urllib2.urlopen( req )
    except urllib2.error.URLError as e:
        if hasattr( e, 'reason' ):
            print( 'Fail in reaching the server -> ', e.reason )
            return False
        elif hasattr( e, 'code' ):
            print( 'The server couldn\'t fulfill the request -> ', e.code )
            return False
    else:
        with open( filename, 'wb' ) as fo:
            fo.write( response.read() )
            #print( 'Url saved as %s' % filename )
        return True

go_comic(go_comics_pages)
go_creator(creator_pages)
go_crankshaft(crankshaft_page)
go_oregon(go_oregon_pages)

for name in images:
    from_url(images[name][0],"SoftwareAssets/public/comics/"+images[name][1]+"/"+name+".jpg")

