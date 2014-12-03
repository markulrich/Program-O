import json, os, random

def print_quote(endpoint):
    with open(endpoint) as f:
        quotes = json.load(f)
    print random.choice(quotes)
    print random.random()

bot_id = 'arnold_schwarzenegger'
endpoint = '../bots/{}/quotes.json'.format(bot_id)
if (os.path.exists(endpoint)):
    print_quote(endpoint)