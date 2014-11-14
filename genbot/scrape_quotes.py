from bs4 import BeautifulSoup
import sys, urllib2

def parseQuotes(html_doc, name):
    soup = BeautifulSoup(html_doc)
    return [elem.contents[0] for elem in soup.find_all('a', title='view quote') if len(elem.contents[0]) > len(name)]

def main():
    name = sys.argv[1]
    endpoint = 'http://www.brainyquote.com/quotes/authors/{}/{}'.format(name[0], name)

    res = []
    i = 0
    for i in range(1, 10): # Read up to 9 pages
        try:
            url = endpoint + (str(i) if i > 1 else '') + '.html'
            req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
            response = urllib2.urlopen(req)
            res += parseQuotes(response.read(), name)
        except urllib2.HTTPError:
            continue
    print res
    exit(0) if i > 1 else exit(1)

if __name__ == '__main__':
    main()