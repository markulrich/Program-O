import string
from textblob import TextBlob

class Features:
    def __init__(self, human_input, quotes):
        self.human_input = human_input
        self.quotes = quotes

    @staticmethod
    def avgWordLen(sentance):
        words = sentance.split()
        return sum(len(w) for w in words) / len(words)

    @staticmethod
    def similarity_word_feature(userInput, quote):
        userInput = userInput.lower()
        quote = quote.lower()
        stripped_input = string.split("".join(c for c in userInput if c not in ('!', '.', ':', '?', ',')))
        stripped_quote = string.split("".join(c for c in quote if c not in ('!', '.', ':', '?', ',')))
        num_same_words = len(set(stripped_input).intersection(set(stripped_quote)))
        num_total_words = len(set(stripped_input + stripped_quote))
        return float(num_same_words) / num_total_words

    # returns 1 if both userInput and quote are questions, 0 otherwise
    @staticmethod
    def question_feature(userInput, quote):
        if (userInput[len(userInput) - 1] == '?' and quote[len(quote) - 1] == '?'):
            return 1
        else:
            return 0

    @staticmethod
    def similarity_nword_feature(userInput, quote, n):

        def find_ngrams(wordList, n):
            return zip(*[wordList[i:] for i in range(n)])

        inputList = userInput.lower().split()
        quoteList = quote.lower().split()
        if (not (len(inputList) >= n and len(quoteList) >= n)):
            return 0

        inputNgramSet = set(find_ngrams(inputList, n))
        quoteNgramSet = set(find_ngrams(quoteList, n))
        num_same_ngrams = len(inputNgramSet.intersection(quoteNgramSet))
        num_total_ngrams = len(inputNgramSet.union(quoteNgramSet))
        return float(num_same_ngrams) / num_total_ngrams

    # returns the proportion of different matching ngrams in userInput and quote in relation to the total number of different ngrams in both
    @staticmethod
    def similarity_ngram_feature(userInput, quote, n):
        userInput = userInput.lower()
        quote = quote.lower()
        stripped_input = "".join(c for c in userInput if c not in ('!', '.', ':', '?', ',', " "))
        stripped_quote = "".join(c for c in quote if c not in ('!', '.', ':', '?', ',', " "))
        total_ngrams = set([])
        same_ngrams = set([])
        if (n <= len(stripped_input) and n <= len(stripped_quote)):
            for i in range(len(stripped_input) - (n - 1)):
                for j in range(len(stripped_quote) - (n - 1)):
                    n_gram_input = stripped_input[i:(i + n)]
                    n_gram_quote = stripped_quote[j:(j + n)]
                    total_ngrams.add(n_gram_input)
                    total_ngrams.add(n_gram_quote)
                    if (n_gram_input == n_gram_quote):
                        if n_gram_input not in same_ngrams:
                            same_ngrams.add(n_gram_input)
            return float(len(same_ngrams)) / len(total_ngrams)

        else:
            return 0

    @staticmethod
    def similar_sentiment_polarity(userInput, quote):
        return abs(TextBlob(userInput).sentiment.polarity - TextBlob(quote).sentiment.polarity)

    @staticmethod
    def similar_sentiment_subjectivity(userInput, quote):
        return abs(TextBlob(userInput).sentiment.subjectivity - TextBlob(quote).sentiment.subjectivity)

    @staticmethod
    def similar_word_lengths(i, q):
        i_av = Features.avgWordLen(i)
        q_av = Features.avgWordLen(q)
        return abs(i_av - q_av) / max(i_av, q_av)

    FEATURES = [
        lambda i, q: abs(2 * len(i) - len(q)) / max(2 * len(i), len(q)),
        lambda i, q: Features.similar_word_lengths(i, q),
        lambda i, q: Features.question_feature(i, q),
        lambda i, q: Features.similarity_nword_feature(i, q, 1),
        lambda i, q: Features.similarity_nword_feature(i, q, 2),
        lambda i, q: Features.similarity_nword_feature(i, q, 3),
        lambda i, q: Features.similarity_nword_feature(i, q, 4),
        lambda i, q: Features.similarity_ngram_feature(i, q, 1),
        lambda i, q: Features.similarity_ngram_feature(i, q, 2),
        lambda i, q: Features.similarity_ngram_feature(i, q, 3),
        lambda i, q: Features.similarity_ngram_feature(i, q, 4),
        lambda i, q: Features.similarity_ngram_feature(i, q, 5),
        lambda i, q: Features.similarity_ngram_feature(i, q, 6),
        lambda i, q: Features.similarity_ngram_feature(i, q, 7),
        lambda i, q: Features.similarity_ngram_feature(i, q, 8),
        lambda i, q: Features.similar_sentiment_polarity(i, q),
        lambda i, q: Features.similar_sentiment_subjectivity(i, q)
    ]

    WEIGHTS = [
        0.,
        0.,
        0.,
        7.27955947,
        3.51367434,
        0.95292548,
        0.,
        -0.05705536,
        5.68781713,
        14.8326,
        12.76462661,
        10.72981724,
        8.36520828,
        6.23124858,
        4.52811743,
        0
    ]

    def getFeats(self, quote):
        return [feat(self.human_input, quote) for feat in Features.FEATURES]

    def getFeatureVectors(self):
        return [self.getFeats(q) for q in self.quotes]

    def getScore(self, quote):
        return sum(p * q for p, q in zip(self.getFeats(quote), Features.WEIGHTS))

    def getBestQuote(self):
        scores = [self.getScore(q) for q in self.quotes]
        ind, score = max(enumerate(scores), key=lambda x: x[1])
        return self.quotes[ind], score