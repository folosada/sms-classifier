from SMSProcessor import SMSProcessor

import pandas as pd
import numpy as np
from os import path

from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from collections import Counter
import matplotlib.pyplot as plt

from datetime import datetime

import re
import functools

import statistics

class SMSStatistics(SMSProcessor):
    
    def _changeDateToMonth(self, value):
        date = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return date.strftime('%B')

    def _changeDateToDayAndMonth(self, value):
        date = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return date.strftime('%d/%B')

    def _wordcloudGraphic(self):
        ## Importing database
        df = pd.read_csv('./sms_database.csv', encoding='latin-1')
        database = df.drop(['Full_Text', 'Common_Word_Count', 'Word_Count', 'Date', 'IsSpam'], axis=1)

        ## Creating word cloud graphic
        wordCloudDict = {}
        words = np.array(database.values)
        words = words.transpose()
        for indexColumn in range(len(words)):
            total = np.sum(words[indexColumn])
            wordCloudDict[database.columns[indexColumn]] = total            
        
        wordcloud = WordCloud(background_color="white").generate_from_frequencies(wordCloudDict)

        ## Ploting and saving to file the word cloud graphic
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(self._outputDir + 'wordcloud.png')
        plt.close()

    def _messagesByMonth(self):
        ## Importing database
        df = pd.read_csv('./sms_database.csv', usecols=['IsSpam', 'Date'], encoding='latin-1')[['IsSpam', 'Date']]
        df.loc[:,'IsSpam'] = df.IsSpam.map({'no':0, 'yes':1})
        df.loc[:,'Date'] = df.Date.map(self._changeDateToMonth)

        ## Adjusting data to messages by month
        database = np.array(df.values)
        monthSpam = {}
        monthCommon = {}
        months = []
        for item in database:
            if not item[1] in months:
                months.append(item[1])
            if (item[0] == 0):
                valueToAdd = (1 if item[0] == 0 else 0)
                monthCommon[item[1]] = (monthCommon[item[1]] + valueToAdd) if item[1] in monthCommon else valueToAdd
            elif (item[0] == 1):
                valueToAdd = (1 if item[0] == 1 else 0)
                monthSpam[item[1]] = (monthSpam[item[1]] + valueToAdd) if item[1] in monthSpam else valueToAdd

        spams = []
        for key, value in monthSpam.items():
            spams.append(value)
        commons = []
        for key, value in monthCommon.items():
            commons.append(value)

        ## Ploting graphic
        barWidth = 0.25

        # Set position of bar on X axis
        r1 = np.arange(len(spams))
        r2 = [x + barWidth for x in r1]
        
        # Make the plot
        plt.bar(r1, spams, color='#7f6d5f', width=barWidth, edgecolor='white', label='Spam Messages')
        plt.bar(r2, commons, color='#557f2d', width=barWidth, edgecolor='white', label='Common Messages')
        
        # Add xticks on the middle of the group bars
        plt.xlabel('Months', fontweight='bold')
        plt.xticks([r + barWidth for r in range(len(spams))], months)
        
        # Create legend & Show graphic
        plt.legend()
        plt.savefig(self._outputDir + 'messages-by-month.png')
        plt.close()

    def _valueByMonth(self, biggest: bool, array: list):
        valueByMonth = {}
        for item in array:
            valueByMonth[item[1]] = (item[0] if (biggest and valueByMonth[item[1]] < item[0]) or (not biggest and valueByMonth[item[1]] > item[0]) else valueByMonth[item[1]]) if item[1] in valueByMonth else item[0]
        return valueByMonth

    def _statistics(self):
        ## Importing database
        df = pd.read_csv('./sms_database.csv', usecols=['Word_Count', 'Date'], encoding='latin-1')        
        df.loc[:,'Date'] = df.Date.map(self._changeDateToMonth)
        biggestByMonth = self._valueByMonth(True, df.values)
        smallerByMonth = self._valueByMonth(False, df.values)

        ## Grouping values by month
        valuesByMonth = {}
        for item in df.values:
            if (item[1] in valuesByMonth):
                valuesByMonth[item[1]].append(item[0])
            else:
                valuesByMonth[item[1]] = [item[0]]

        ## Getting statistics values
        averageByMonth = {}
        medianByMonth = {}
        varianceByMonth = {}
        standardDeviationByMonth = {}
        for key, value in valuesByMonth.items():
            averageByMonth[key] = statistics.mean(value)
            medianByMonth[key] = statistics.median(value)
            standardDeviationByMonth[key] = statistics.pstdev(value)
            varianceByMonth[key] = statistics.pvariance(value)

        ## Printing results
        print('\nStatistics by Month\n')
        print('Max: {}'.format(biggestByMonth))
        print('Min: {}'.format(smallerByMonth))
        print('Average: {}'.format(averageByMonth))
        print('Median: {}'.format(medianByMonth))
        print('Standard Deviation: {}'.format(standardDeviationByMonth))
        print('Variance: {}\n'.format(varianceByMonth))     
    
    def _dayWithMoreCommonMessages(self):
        df = pd.read_csv('./sms_database.csv', usecols=['IsSpam', 'Date'], encoding='latin-1')        
        df.loc[:,'IsSpam'] = df.IsSpam.map({'no': 1, 'yes': 0})
        df.loc[:,'Date'] = df.Date.map(self._changeDateToDayAndMonth)
        months = {}
        daysOfMonth = {}
        for item in df.values:
            daysOfMonth[item[0]] = (daysOfMonth[item[0]] + item[1]) if item[0] in daysOfMonth else item[1]

        for key, value in daysOfMonth.items():
            monthName = key[3:]
            day = key[:2]
            if monthName in months:
                if months[monthName]['messages'] < int(value):
                    months[monthName] = {'day': day, 'messages': value}
            else:
                months[monthName] = {'day': day, 'messages': value}            
        
        print('\nDay of the Month with more Common Messages\n')
        for key, value in months.items():
            print('Month: {}'.format(key))
            print('Day: {}'.format(value['day']))
            print('Common messages: {}'.format(value['messages']))        
        print('')

    def run(self):
        self._wordcloudGraphic()
        self._messagesByMonth()
        self._statistics()
        self._dayWithMoreCommonMessages()

SMSStatistics().run()        
