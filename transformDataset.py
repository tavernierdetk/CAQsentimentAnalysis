import json
import csv
import pandas as pd
import datetime
import sentimentAnalysis
import pickle
from emoji import UNICODE_EMOJI

def has_emoji(text):
    for emoji in UNICODE_EMOJI:
        if text.find(emoji) >= 0:
            return 1
    return 0

def exclamationMark(text):
    if text.find('!') >= 0:
        return 1
    return 0

def listCheck(text, listDict):
    for i in listDict:
        if text.find(i) > -1:
            return 1
    return 0

def averageSentiment(textArray, analyser):
    runningTotal = 0
    for text in textArray:
        runningTotal += analyser.polarity_scores(text)['compound']
    return runningTotal/len(textArray)

def averagegWordLength(text):
    tokens = text.split()
    runningTotal = 0
    for token in tokens:
        runningTotal += len(token)
    return runningTotal/len(tokens)

def transformAndSave(inputfilepath):
    with open(inputfilepath, 'rb') as file:
        jsonData = json.load(file)

    data_row = {
        'message': [],
        'sentiment': [],
        'day_of_month': [],
        'day_posted': [],
        'time_of_day_posted': [],

        'length_of_post': [],
        'type_of_post': [],
        'emoji_included': [],
        'mentions_other_political_party': [],
        'exclamation_mark': [],
        'avg_word_length': [],
        'number_of_shares': [],
        'number_of_comments': [],
        'avg_comment_sentiment': [],
        'is_popular': []
    }
    count = 0


    # load other parties
    otherPartiesDict = [
        'PLQ','gouvernement libéral','administration libérale' ,'libéraux' ,'régime libéral','PLT' ,'PQ'
    ]


    
    
    
    for post in jsonData:
        if 'comments' not in post:
            continue
        elif 'message' not in post:
            continue
        elif 'status_type' not in post:
            continue
        else:
            # initialise vader sentiment analyser with default lexicon
            analyser = sentimentAnalysis.setupAnalyser()

            # extract and format date
            date_string = post['created_time']
            full_date = datetime.datetime.strptime(date_string[:-5], '%Y-%m-%dT%H:%M:%S')

            message = post["message"]

            comments_array = []
            for i in post['comments']:
                comments_array.append(i["message"])

            if full_date.hour in [22,23,0,1,2,3,4,5]:
                data_row['time_of_day_posted'].append('nuit')
            elif full_date.hour in [6,7,8]:
                data_row['time_of_day_posted'].append('matin')
            elif full_date.hour in [9,10,11]:
                data_row['time_of_day_posted'].append('am')
            elif full_date.hour in [12,13,14,15,16]:
                data_row['time_of_day_posted'].append('pm')
            elif full_date.hour in [17,18,19,20,21]:
                data_row['time_of_day_posted'].append('soiree')

            data_row['message'].append(message)
            data_row['sentiment'].append(analyser.polarity_scores(message)['compound'])

            data_row['day_posted'].append(full_date.weekday())
            data_row['day_of_month'].append(full_date.day)
             # number of words
            data_row['length_of_post'].append(len(message.split()))
            data_row['type_of_post'].append(post['status_type'])
            data_row['emoji_included'].append(has_emoji(message))
            data_row['mentions_other_political_party'].append(listCheck(message, otherPartiesDict))
            data_row['exclamation_mark'].append(exclamationMark(message))
            data_row['avg_word_length'].append(averagegWordLength(message))
            if 'shares' in post:
                if post['shares']['count'] > 30:
                    data_row['number_of_shares'].append(1)
                else:
                    data_row['number_of_shares'].append(0)
            else:
                data_row['number_of_shares'].append(0)

            if 'comments' in post:
                data_row['number_of_comments'].append(len(post['comments']))
            else:
                data_row['number_of_comments'].append(0)
            data_row['avg_comment_sentiment'].append(averageSentiment(comments_array, analyser))
            data_row['is_popular'].append(post["is_popular"])
            print(count)
            count +=1


    df = pd.DataFrame(data=data_row)
    df3 = df['message']
    df = df.drop(columns=['message'])
    df = pd.get_dummies(df, prefix=['time_of_day_posted','type_of_post'])
    df2 = pd.get_dummies(df['day_posted'], prefix='day_posted')
    df = pd.concat([df,df2,df3], axis=1)
    with open('pickleFiles/dfFromJson.pkl', 'wb') as file:
        pickle.dump(df, file)
    return df

if __name__ == "__main__":
    input_filepath = "JSONFiles/caqai-414e9-FB_POSTS-export.json"
    transformAndSave(input_filepath)
