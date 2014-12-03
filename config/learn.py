from sklearn.linear_model import SGDClassifier
from features import Features


def main():
    training_data = {}

    questions = ["What are your hobbies?", "What do you think about America?",
                 "Is money important to you?", "What is the meaning of life?",
                 "What do you think people think of you?", "Do you think that you have been successful?",
                 "What are your political views?", "What are your environmental views?",
                 "What do you think about gay marriage?", "What is most important for the country?"]

    quotes = [
        "My own dreams fortunately came true in this great state. I became Mr. Universe; I became a successful businessman. And even though some people say I still speak with a slight accent, I have reached the top of the acting profession.",
        "Even with my divorce and with everything, I don't need money.",
        "No matter the nationality, no matter the religion, no matter the ethnic background, America brings out the best in people.",
        "I believe with all my heart that America remains 'the great idea' that inspires the world. It is a privilege to be born here. It is an honor to become a citizen here. It is a gift to raise your family here, to vote here, and to live here.",
        "People should make up their own mind about what they think of me.",
        "As long as I live, I will never forget that day 21 years ago when I raised my hand and took the oath of citizenship. Do you know how proud I was? I was so proud that I walked around with an American flag around my shoulders all day long.",
        "Government's first duty and highest obligation is public safety.",
        "You know, nothing is more important than education, because nowhere are our stakes higher; our future depends on the quality of education of our children today.",
        "There is no place, no country, more compassionate more generous more accepting and more welcoming than the United States of America.",
        "I'm addicted to exercising and I have to do something every day.",
        "The future is green energy, sustainability, renewable energy.",
        "For me life is continuously being hungry. The meaning of life is not simply to exist, to survive, but to move ahead, to go up, to achieve, to conquer.",
        "We are a forward-looking people, and we must have a forward-looking government.",
        "I think that gay marriage should be between a man and a woman.",
        "Money doesn't make you happy. I now have $50 million but I was just as happy when I had $48 million."]

    # Everything is 0 based
    training_data[questions[0]] = [9]
    training_data[questions[1]] = [2, 3, 5, 8]
    training_data[questions[2]] = [1, 14]
    training_data[questions[3]] = [11]
    training_data[questions[4]] = [4]
    training_data[questions[5]] = [0]
    training_data[questions[6]] = [12, 6]
    training_data[questions[7]] = [10]
    training_data[questions[8]] = [13]
    training_data[questions[9]] = [7]

    good_matches = [
        [9],
        [2, 3, 5, 8],
        [1, 14],
        [11],
        [4],
        [0],
        [12, 6],
        [10],
        [13],
        [7]
    ]

    X = []
    y = []

    for matches, human_input in zip(good_matches, questions):
        X_part = Features(human_input, quotes).getFeatureVectors()
        X += X_part
        y_part = [0] * len(X_part)

        print 'Matches for %s:' % human_input
        for i in matches:
            y_part[i] = 1
            print '\t%s' % quotes[i]
        y += y_part

    clf = SGDClassifier(loss="hinge", penalty="l2")
    clf.fit(X, y)
    print 'Based on %d points, coefficients are:' % len(X)
    print clf.coef_


if __name__ == '__main__':
    main()
