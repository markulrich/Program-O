from bs4 import BeautifulSoup
import sys, urllib2, json, os

QUOTES_FILE = 'quotes.json'

def parseQuotes(html_doc, name):
    soup = BeautifulSoup(html_doc)
    return {str(elem.contents[0]) for elem in soup.find_all('a', title='view quote') if len(elem.contents[0]) > len(name)}

def main():
    name = sys.argv[1]
    directory = '../bots/{}/'.format(name)
    if os.path.exists(directory + QUOTES_FILE):
        return

    endpoint = 'http://www.brainyquote.com/quotes/authors/{}/{}'.format(name[0], name)

    res = set()
    i = 1
    for i in range(1, 10): # Read up to 9 pages
        try:
            url = endpoint + ('_' + str(i) if i > 1 else '') + '.html'
            req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
            response = urllib2.urlopen(req)
            res |= parseQuotes(response.read(), name)
        except urllib2.HTTPError:
            continue
    if i == 1:
        exit(1)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(directory + QUOTES_FILE, 'w') as of:
        json.dump(list(res), of)

if __name__ == '__main__':
    main()