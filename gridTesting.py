import sentimentAnalysis
from emoji import UNICODE_EMOJI
import datetime
import pandas as pd
import pickle

class Post:
    def __init__(self, text, datetime, typeOfPost):
        self.type_of_post = typeOfPost
        self.text =         {
            'value': text,
            'test_step':1,
            'test_range': (0,1),
            'status': 'function',
            'method': ""
        }
        self.datetime =         {
            'value': datetime,
            'test_step':1,
            'test_range': (0,1),
            'status': 'function',
            'method': ""
        }
        self.analyser = sentimentAnalysis.setupAnalyser()
        self.sentiment =        {
            'value': self.analyser.polarity_scores(self.text['value'])['compound'],
            'test_step':.1,
            'test_range': (-1, 1),
            'status': 'train',
            'method': ""
        }

        self.day_of_month = {
            'value': datetime.day,
            'test_step':1,
            'test_range': (0, 31),
            'status': 'train',
            'method': ""
        }

        self.length_of_post = {
            'value': len(self.text['value'].split()),
            'test_step':5,
            'test_range': (0, 300),
            'status': 'train',
            'method': ""
        }



        self.has_emoji()
        self.exclamation_mark()

        self.avg_word_length = {
            'value': self.averagegWordLength(),
            'test_step':.2,
            'test_range': (3, 10),
            'status': 'train',
            'method': ""
        }

        self.time_of_day_posted_am = 0
        self.time_of_day_posted_nuit = 0
        self.time_of_day_posted_matin = 0
        self.time_of_day_posted_pm = 0
        self.time_of_day_posted_soiree = 0
        self.type_of_post_added_photos = 0
        self.type_of_post_added_video = 0
        self.type_of_post_mobile_status_update = 0
        self.type_of_post_shared_story = 0
        self.day_posted_0 = 0
        self.day_posted_1 = 0
        self.day_posted_2 = 0
        self.day_posted_3 = 0
        self.day_posted_4 = 0
        self.day_posted_5 = 0
        self.day_posted_6 = 0
        self.similarity_famille = 0
        self.similarity_education = 0
        self.similarity_travail = 0
        self.similarity_argent = 0
        self.convertHour()
        self.convertDay()
        self.listOtherParties = [
        'PLQ','gouvernement libéral','administration libérale' ,'libéraux' ,'régime libéral','PLT' ,'PQ']
        self.mentions_other_political_party = self.listCheck(self.listOtherParties)
        self.createDF()

    def updateTypeOfPost(self):
        if self.type_of_post == 'shared_story':
            self.type_of_post_shared_story = 1
        elif self.type_of_post == 'added_photos':
            self.type_of_post_added_photos = 1
        elif self.type_of_post == 'added_video':
            self.type_of_post_added_video = 1
        elif self.type_of_post == 'mobile_status_update':
            self.type_of_post_mobile_status_update = 1

    def convertHour(self):
        if self.datetime['value'].hour in [22, 23, 0, 1, 2, 3, 4, 5]:
            self.time_of_day_posted_nuit = 1
        elif self.datetime['value'].hour in [6, 7, 8]:
            self.time_of_day_posted_matin = 1
        elif self.datetime['value'].hour in [9, 10, 11]:
            self.time_of_day_posted_am = 1
        elif self.datetime['value'].hour in [12, 13, 14, 15, 16]:
            self.time_of_day_posted_pm = 1
        elif self.datetime['value'].hour in [17, 18, 19, 20, 21]:
            self.time_of_day_posted_soiree = 1

    def convertDay(self):
        if self.datetime['value'].day == 0:
            self.day_posted_0 = 1
        if self.datetime['value'].day == 1:
            self.day_posted_1 = 1
        if self.datetime['value'].day == 2:
            self.day_posted_2 = 1
        if self.datetime['value'].day == 3:
            self.day_posted_3 = 1
        if self.datetime['value'].day == 4:
            self.day_posted_4 = 1
        if self.datetime['value'].day == 5:
            self.day_posted_5 = 1
        if self.datetime['value'].day == 6:
            self.day_posted_6 = 1

    def createDF(self):
        data = {
            'sentiment': [self.sentiment['value']],
            'day_of_month': [self.day_of_month['value']],
            'length_of_post': [self.length_of_post['value']],
            'emoji_included': [self.emoji_included],
            'mentions_other_political_party': [self.mentions_other_political_party],
            'exclamation_mark': [self.exclamation_mark],
            'avg_word_length': [self.avg_word_length['value']],
            'time_of_day_posted_am': [self.time_of_day_posted_am],
            'time_of_day_posted_matin': [self.time_of_day_posted_matin],
            'time_of_day_posted_nuit': [self.time_of_day_posted_nuit],
            'time_of_day_posted_pm': [self.time_of_day_posted_pm],
            'time_of_day_posted_soiree': [self.time_of_day_posted_soiree],
            'type_of_post_added_photos': [self.type_of_post_added_photos],
            'type_of_post_added_video': [self.type_of_post_added_video],
            'type_of_post_mobile_status_update': [self.type_of_post_mobile_status_update],
            'type_of_post_shared_story': [self.type_of_post_shared_story],
            'day_posted_0': [self.day_posted_0],
            'day_posted_1': [self.day_posted_1],
            'day_posted_2': [self.day_posted_2],
            'day_posted_3': [self.day_posted_3],
            'day_posted_4': [self.day_posted_4],
            'day_posted_5': [self.day_posted_5],
            'day_posted_6': [self.day_posted_6],
            'similarity_famille': [self.similarity_famille],
            'similarity_education': [self.similarity_education],
            'similarity_travail': [self.similarity_travail],
            'similarity_argent': [self.similarity_argent]
        }
        df = pd.DataFrame(data)
        self.df = df

    def has_emoji(self):
        for emoji in UNICODE_EMOJI:
            if self.text['value'].find(emoji) >= 0:
                self.emoji_included = 1
                return
        self.emoji_included = 0

    def exclamation_mark(self):
        if self.text['value'].find('!') >= 0:
            self.exclamation_mark = 1
            return
        self.exclamation_mark = 0

    def give_pred(self,model):
        predictions = model.predict_proba(self.df)
        return predictions[0][1]

    def listCheck(self, listDict):
        for i in listDict:
            if self.text['value'].find(i) > -1:
                return 1
        return 0

    def averagegWordLength(self):
        tokens = self.text['value'].split()
        runningTotal = 0
        for token in tokens:
            runningTotal += len(token)
        return runningTotal / len(tokens)

if __name__ == "__main__":
    now = datetime.datetime.now()
    time = datetime.datetime(2020, 4, 16, 17, 40, 54, 3)
    testPost = Post(
        """
        Nous sommes fiers d'annoncer la candidature de Rachel Bourdon dans la circonscription de Hull.
Rachel a occupé le poste d’infirmière clinicienne en psychiatrie à l’urgence de l’hôpital de St-Mary tout en complétant un diplôme d’études supérieures spécialisées (DESS) en gestion à l’École des hautes études commerciales (HEC) de Montréal.
Gatinoise d’adoption, elle a rapidement remarqué les déficits dans les services de première ligne et d’obstétrique sans compter le personnel soignant à bout de souffle. Elle est aussi préoccupée par les problèmes de pauvreté, de même que les difficultés dans le réseau de l’éducation.
Bienvenue dans l'équipe du changement!
        """,
        time, 'added_photos')
    with open('pickleFiles/model.pkl', 'rb') as file:
        model = pickle.load(file)

    print(testPost.give_pred(model))


    attributes_to_gridSearch = ['sentiment', 'length_of_post']
    for attribute in attributes_to_gridSearch:
        propObject = getattr(testPost,attribute)
        originalValue = propObject['value']
        print(originalValue)
        multiple = 1/propObject['test_step']
        start = int(propObject['test_range'][0]*multiple)
        stop = int((propObject['test_range'][1]*multiple)+1)
        step = int(propObject['test_step']*multiple)


        for i in range(start, stop , step):
            testValue = i/multiple
            propObject['value'] = testValue
            setattr(testPost,attribute , propObject)
            testPost.createDF()
            print(attribute, testValue, testPost.give_pred(model))
        propObject['value'] = originalValue
        setattr(testPost, attribute, propObject)







