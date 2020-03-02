# SMS Classifier

## Purpose

The puporse of this project is read a CSV file with SMSs and others data already extracted from SMSs, like common words, words by SMS, the SMS is an spam or not, etc.
With this data the follow items will be shown.

- <a name=purpose_step_1></a>Step 1:
   - A word cloud graphic containing the most frequently words from the database.
   - A graphic containing the commons messages and spam message by month.
   - The calculation of the maximum, minimum, average, median, standard deviation and variance of the total number of words.
   - The day of each month that contains the largest sequence of common messages received (not spam).

- <a name=purpose_step_2></a>Step 2:
   - A way to classify the SMSs between common messages and spam messages.

## Prerequisites

- [Python 3.8.2](https://www.python.org/downloads/)
   - Numpy
      - `pip install numpy`
   - Wordcloud
      - `pip install wordcloud`
   - Pandas
      - `pip install Pandas`
   - Scikit Learn
      - `pip install -U scikit-learn`

## Running

- After clone the project, run the command `python Main.py`
- Choose between the two steps:
   - Step 1: Show the graphics and results described in item [Step 1](#purpose_step_1)
   - Step 2: Classify the SMSs from the file `sms_database.csv` between common messages and spam messages, like [Step 2](#purpose_step_2) describes. This step uses the (Naive Bayes classifier)[https://en.wikipedia.org/wiki/Naive_Bayes_classifier] to classify the SMSs. 

## Results

- Step 1:

- Step 2:
   - The results will be printed in console and the files `output.csv` and `output-difference.csv` will be create in folder `./output/`. The two files has 3 columns
      - Column: `IsSpam`: This column contain the original data from database if the message is a spam or common message.
      - Column: `IsSpam-Prediction`: This column contain the information calculate by Naive Bayes classifier if the message is a spam or common message.
      - Column: `Full_Text`: This column contain the messages from the original database.
   - File `output.csv`
      - This file contains all messages from the database. Is a CSV file with 3 columns.
   - File `output-difference.csv`
      - This file contains only the messages that the Naive Bayes classifier misclassified. That is, only the records with the `IsSpam` and `IsSpam-Prediction` columns that have different values.