from bs4 import BeautifulSoup
import sys, urllib2, json, os

QUOTES_FILE = 'quotes.json'

def parseQuotes(html_doc, name):
    soup = BeautifulSoup(html_doc)
    return {str(elem.contents[0]) for elem in soup.find_all('a', title='view quote') if len(elem.contents[0]) > len(name)}

def main():
    name = sys.argv[1]
    directory = '../bots/{}/'.format(name)
    fileName = directory + QUOTES_FILE
    if os.path.exists(fileName):
        print 'File {} already exists'.format(fileName)
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
            break
    if i == 1:
        print 'Sorry could not find any quotes for {}, please use format firstname_lastname.'.format(name)
        exit(1)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(fileName, 'w') as of:
        print 'Outputing file to {}'.format(fileName)
        json.dump(list(res), of)

if __name__ == '__main__':
    main()