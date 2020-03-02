from SMSProcessor import SMSProcessor

import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


class SMSClassifier(SMSProcessor):
    
    def run(self):
        ## Opening database file
        smsCsv = pd.read_csv('./sms_database.csv', usecols=['Full_Text', 'IsSpam'], encoding='latin-1')[['IsSpam', 'Full_Text']]
        smsCsv = smsCsv.rename(columns={'IsSpam':'label', 'Full_Text':'sms'})
        smsCsv.loc[:,'label'] = smsCsv.label.map({'no':0, 'yes':1})

        texts = smsCsv.sms
        labels = smsCsv.label

        ## Split the data between training data and test data, using sklearn
        xTrain, xTest, yTrain, yTest = train_test_split(texts, labels, test_size=0.20, random_state=1)

        countVector = CountVectorizer()
        trainingData = countVector.fit_transform(xTrain)
        testingData = countVector.transform(xTest)

        ## Use the Naive Bayes classifier
        naiveBayes = MultinomialNB()
        ## Train the machine
        naiveBayes.fit(trainingData, yTrain)

        ## Run the tests and print the results
        predictions = naiveBayes.predict(testingData)

        print('Testing Data\n')
        print('Accuracy score: {}'.format(accuracy_score(yTest, predictions)))
        print('Precision score: {}'.format(precision_score(yTest, predictions)))
        print('Recall score: {}'.format(recall_score(yTest, predictions)))
        print('F1 score: {}\n'.format(f1_score(yTest, predictions)))

        ## Run the classifier over the full database
        classificationData = countVector.transform(texts)
        predictions = naiveBayes.predict(classificationData)

        print('Classification results\n')        
        print('Accuracy score: {}'.format(accuracy_score(labels, predictions)))
        print('Precision score: {}'.format(precision_score(labels, predictions)))
        print('Recall score: {}'.format(recall_score(labels, predictions)))
        print('F1 score: {}\n'.format(f1_score(labels, predictions)))
        
        ## Format the output to save .csv file
        output = [smsCsv.label.values, predictions, smsCsv.sms.values]        
        outputText = 'isSpam,isSpam-Prediction,Full_Text\n'
        differenceOutputText = 'isSpam,isSpam-Prediction,Full_Text\n'
        length = len(output[1])
        for index in range(length):
            line = ('Yes' if output[0][index] == 1 else 'No')  + ',' + ('Yes' if output[1][index] == 1 else 'No') + ',"' + output[2][index] + '"\n'
            outputText = outputText + line
            if (output[0][index] != output[1][index]):
                differenceOutputText = differenceOutputText + line
        file = open(self._outputDir + 'output.csv', 'w', encoding='utf8')
        file.write(outputText)
        file.close()
        file = open(self._outputDir + 'output-difference.csv', 'w', encoding='utf8')
        file.write(differenceOutputText)
        file.close()