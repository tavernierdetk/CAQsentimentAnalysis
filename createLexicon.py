def createLexicon(positiveWords, negativeWords):
    f = open("Dictionaries/frenchLexicon.txt", "w+")

    for i in positiveWords:
        f.write(i + '\t' + '1' + '\t' + '1'+ '\n')

    for i in negativeWords:
        f.write(i + '\t' + '-1' + '\t' + '1'+ '\n')


    f.write("neutral\t0")
    f.close()

def addFromLexicon(listToAdd, filepath):
    f = open(filepath,'r')
    lines = f.readlines()
    for line in lines:
        listToAdd.append(line[:-1])
    return listToAdd


if __name__ == "__main__":
    positiveWords = []
    negativeWords = []

    addFromLexicon(positiveWords,'Dictionaries/positive_words_fr.txt')
    addFromLexicon(negativeWords,'Dictionaries/negative_words_fr.txt')

    for i in positiveWords:
        print(i)

    createLexicon(positiveWords,negativeWords)

