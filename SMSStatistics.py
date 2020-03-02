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

class SMSStatistics(SMSProcessor):
    
    def _changeDateToMonth(self, value):
        date = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')        
        ##monthNumber = re.sub(r'\d{2}/(\d{2})/d{4}\s*\d{2}:d{2}', r'\1', value)
        return date.strftime('%B')

    def run(self):
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
        
        

SMSStatistics().run()        
