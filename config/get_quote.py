import json, os, random, sys

class Features:
    def __init__(self, human_input, quotes):
        self.human_input = human_input
        self.quotes = quotes

    @staticmethod
    def avgWordLen(sentance):
        words = sentance.split()
        return sum(len(w) for w in words) / len(words)

    FEATURES = [
        lambda i, q: abs(2 * len(i) - len(q)),
        lambda i, q: abs(Features.avgWordLen(i) - Features.avgWordLen(q))
    ]

    WEIGHTS = [
        -5.0,
        -2.0
    ]

    def getFeats(self, quote):
        return [feat(self.human_input, quote) for feat in Features.FEATURES]

    def getScore(self, quote):
        return sum(p * q for p, q in zip(self.getFeats(quote), Features.WEIGHTS))

    def getBestQuote(self):
        scores = [self.getScore(q) for q in self.quotes]
        ind, score = max(enumerate(scores), key=lambda x: x[1])
        return self.quotes[ind], score

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