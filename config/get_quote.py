import json, os, random, sys, string

class Features:
    def __init__(self, human_input, quotes):
        self.human_input = human_input
        self.quotes = quotes

    @staticmethod
    def avgWordLen(sentance):
        words = sentance.split()
        return sum(len(w) for w in words) / len(words)

    @staticmethod
    def similarity_word_feature(userInput,quote):
        userInput = userInput.lower()
        quote = quote.lower()
        stripped_input = string.split("".join(c for c in userInput if c not in ('!','.',':','?',',')))
        stripped_quote = string.split("".join(c for c in quote if c not in ('!','.',':','?',',')))
        num_same_words = len(set(stripped_input).intersection(set(stripped_quote)))
        num_total_words = len(set(stripped_input+stripped_quote))
        return float(num_same_words)/num_total_words

    # returns 1 if both userInput and quote are questions, 0 otherwise
    @staticmethod
    def question_feature(userInput,quote):
        if (userInput[len(userInput)-1] == '?' and quote[len(quote)-1]=='?'): return 1
        else: return 0



    # returns the proportion of different matching ngrams in userInput and quote in relation to the total number of different ngrams in both
    @staticmethod
    def similarity_ngram_feature(userInput,quote):
        n = 3 #defines range of n_gram
        userInput = userInput.lower()
        quote = quote.lower()
        stripped_input = "".join(c for c in userInput if c not in ('!','.',':','?',','," "))
        stripped_quote = "".join(c for c in quote if c not in ('!','.',':','?',','," "))
        total_ngrams = set([])
        same_ngrams = set([])
        if (n<=len(stripped_input) and n<=len(stripped_quote)):
            for i in range(len(stripped_input)-(n-1)):
                for j in range(len(stripped_quote)-(n-1)):
                    n_gram_input = stripped_input[i:(i+n)]
                    n_gram_quote = stripped_quote[j:(j+n)]
                    total_ngrams.add(n_gram_input)
                    total_ngrams.add(n_gram_quote)
                    if (n_gram_input == n_gram_quote):
                        if n_gram_input not in same_ngrams:
                            same_ngrams.add(n_gram_input)
            return float(len(same_ngrams))/len(total_ngrams)

        else: return 0

    @staticmethod
    def similar_word_lengths(i, q):
        i_av = Features.avgWordLen(i)
        q_av = Features.avgWordLen(q)
        return abs(i_av - q_av) / max(i_av, q_av)

    FEATURES = [
        lambda i, q: 1 - abs(2 * len(i) - len(q)) / max(2 * len(i), len(q)),
        lambda i, q: 1 - Features.similar_word_lengths(i, q),
        lambda i, q: Features.similarity_word_feature(i, q),
        lambda i, q: 1 - Features.question_feature(i, q),
        lambda i, q: Features.similarity_ngram_feature(i, q)
    ]

    WEIGHTS = [
        5.0,
        2.0,
        80,
        30,
        2
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