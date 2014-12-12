from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
from features import Features
import numpy as np
from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC

import numpy as np
from scipy import interp
import matplotlib.pyplot as plt

from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc
from sklearn.cross_validation import StratifiedKFold

def get_data():
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

    return X, y

def main():
    X, y = get_data()

    clf = SGDClassifier(loss="hinge", penalty="l2")
    clf.fit(X, y)
    print 'predicts:'
    print clf.predict(X)
    print 'Based on %d points, coefficients are:' % len(X)
    print clf.coef_[0]

    models = [SGDClassifier(loss="hinge", penalty="l1"),
              RandomForestClassifier(n_estimators=10),
              svm.SVC(),
              tree.DecisionTreeClassifier()]

    kf = cross_validation.KFold(len(X), n_folds=10, shuffle=True)
    X = np.array(X)
    y = np.array(y)
    clf = SGDClassifier(loss="hinge", penalty="l2")
    clf.fit(X, y)
    print 'Based on %d points, coefficients are:' % len(X)
    print clf.coef_
    print 'SCORES'
    for m in models:
        scores = kf.cross_val_score(m, X, y, cv=10)
        print "Accuracy: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std())

def grid_search():
    X, y = get_data()

    # Split the dataset in two equal parts
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.5, random_state=0)

    # Set the parameters by cross-validation
    tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                         'C': [1e4, 1e5, 1e6]},
                        {'kernel': ['linear'], 'C': [1e3, 1e4, 1e5, 1e6]}]

    scores = ['precision', 'recall']

    for score in scores:
        print("# Tuning hyper-parameters for %s" % score)
        print()

        clf = GridSearchCV(SVC(C=1), tuned_parameters, cv=5, scoring=score)
        clf.fit(X_train, y_train)

        print("Best parameters set found on development set:")
        print()
        print(clf.best_estimator_)
        print()
        print("Grid scores on development set:")
        print()
        for params, mean_score, scores in clf.grid_scores_:
            print("%0.3f (+/-%0.03f) for %r"
                  % (mean_score, scores.std() / 2, params))
        print()

        print("Detailed classification report:")
        print()
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.")
        print()
        y_true, y_pred = y_test, clf.predict(X_test)
        print(classification_report(y_true, y_pred))
        print()

def plot_roc():
    X, y = get_data()

    # Run classifier with cross-validation and plot ROC curves
    cv = StratifiedKFold(y, n_folds=6)
    classifier = svm.SVC(kernel='linear', C=1e4)

    mean_tpr = 0.0
    mean_fpr = np.linspace(0, 1, 100)
    all_tpr = []

    for i, (train, test) in enumerate(cv):
        probas_ = classifier.fit(X[train], y[train]).predict_proba(X[test])
        # Compute ROC curve and area the curve
        fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
        mean_tpr += interp(mean_fpr, fpr, tpr)
        mean_tpr[0] = 0.0
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, lw=1, label='ROC fold %d (area = %0.2f)' % (i, roc_auc))

    plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')

    mean_tpr /= len(cv)
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    plt.plot(mean_fpr, mean_tpr, 'k--',
             label='Mean ROC (area = %0.2f)' % mean_auc, lw=2)

    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()

if __name__ == '__main__':
    plot_roc()
