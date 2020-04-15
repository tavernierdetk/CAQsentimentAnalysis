from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def setupAnalyser(dictFilePath='/Users/alex/PycharmProjects/CAQSentimentAndPopularityPredictions/Dictionaries/frenchLexicon.txt'):
    analyser = SentimentIntensityAnalyzer()
    analyser.lexicon = {}
    with open(dictFilePath, encoding='utf-8') as f:
        analyser.lexicon_full_filepath = f.read()
    analyser.lexicon = analyser.make_lex_dict()
    return analyser



if __name__ == '__main__':
    print('go')
