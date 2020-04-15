import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import numpy as np
import operator

class TermExtractor:
    def __init__(self, period_length, number_of_terms):
        self.period_length = period_length
        self.number_of_terms = number_of_terms
        self.corpus = []
        self.dictionary = {}
        self.matrix = []
        self.most_relevant = []

    def fitAndTransform(self, corpus):
        itemizer = TfidfVectorizer()
        itemizer.input = corpus
        self.matrix = itemizer.fit_transform(corpus).todense()
        self.dictionary = itemizer.vocabulary_
        print(self.dictionary)
        self.extractMostRelevant()

    def extractMostRelevant(self):
        self.matrix[self.matrix == 0] = np.nan
        means = np.nanmean(self.matrix, axis=0).tolist()
        for index, i in enumerate(means[0]):
            for key, value in self.dictionary.items():
                if (value == index):
                    self.dictionary[key] = {'index':value, 'averageTFIDF':i}
                    print(value)
        dictTuple = []
        for i in self.dictionary:

            dictTuple.append((i, self.dictionary[i]['averageTFIDF'], self.dictionary[i]['index']))
        dictTuple.sort(key=operator.itemgetter(1), reverse=True)
        for i in range(0, self.number_of_terms):
            self.most_relevant.append(dictTuple[i])


if __name__ == "__main__":

    with open('pickleFiles/comments_corpus.pkl', 'rb') as file:
        corpus = pickle.load(file)

    extractor = TermExtractor(12, 6)
    extractor.fitAndTransform(corpus)
    print(extractor.most_relevant)
