import json
import os
import random
import sys

from features import Features

def print_quote(endpoint, human_input):
    with open(endpoint) as f:
        quotes = json.load(f)
    if human_input == '':
        print random.choice(quotes)
        print 0
        return
    f = Features(human_input, quotes)
    quote, score = f.getBestQuote()
    print quote
    print score

def main():
    if len(sys.argv) < 2:
        print 'ERROR0498283 must give name'
        exit(33)
    bot_id = sys.argv[1]
    endpoint = '../bots/{}/quotes.json'.format(bot_id)
    if (os.path.exists(endpoint)):
        print_quote(endpoint, ' '.join(sys.argv[2:]))

if __name__ == '__main__':
    main()