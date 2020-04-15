import sentimentAnalysis
from emoji import UNICODE_EMOJI
import datetime
import pandas as pd
import pickle

class Post:
    def __init__(self, text, datetime):
        self.text = text
        self.datetime = datetime
        self.analyser = sentimentAnalysis.setupAnalyser()
        self.sentiment = self.analyser.polarity_scores(self.text)['compound']
        self.day_of_month = datetime.day
        self.length_of_post = 0
        self.emoji_included = 0
        self.mentions_other_political_party = 0
        self.exclamation_mark()
        self.avg_word_length = 0
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
        self.df = self.createDF()
        self.convertHour()


    def convertHour(self):
        if self.datetime.hour in [22, 23, 0, 1, 2, 3, 4, 5]:
            self.time_of_day_posted_nuit = 1
        elif self.datetime.hour in [6, 7, 8]:
            self.time_of_day_posted_matin = 1
        elif self.datetime.hour in [9, 10, 11]:
            self.time_of_day_posted_am = 1
        elif self.datetime.hour in [12, 13, 14, 15, 16]:
            self.time_of_day_posted_pm = 1
        elif self.datetime.hour in [17, 18, 19, 20, 21]:
            self.time_of_day_posted_soiree = 1

    def createDF(self):
        data = {
            'sentiment': [self.sentiment],
            'day_of_month': [self.day_of_month],
            'length_of_post': [self.length_of_post],
            'emoji_included': [self.emoji_included],
            'mentions_other_political_party': [self.mentions_other_political_party],
            'exclamation_mark': [self.exclamation_mark],
            'avg_word_length': [self.avg_word_length],
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
        return df

    def has_emoji(self):
        for emoji in UNICODE_EMOJI:
            if self.text.find(emoji) >= 0:
                self.emoji_included = 1
                return
        self.emoji_included = 0

    def exclamation_mark(self):
        if self.text.find('!') >= 0:
            self.exclamation_mark = 1
            return
        self.exclamation_mark = 0

    def give_pred(self,model):
        predictions_bool = model.predict(self.df)
        predictions = model.predict_proba(self.df)
        print(predictions)
        print(predictions_bool)
        return

if __name__ == "__main__":
    now = datetime.datetime.now()
    testPost = Post('bonjour a tous chers electeurs, chers citoyens beau, bon, joyeux, consommateurs!', now)
    print(testPost.exclamation_mark)
    with open('pickleFiles/model.pkl', 'rb') as file:
        model = pickle.load(file)
    testPost.give_pred(model)


