# SMS Classifier

## Purpose

The puporse of this project is read a CSV file with SMSs and others data already extracted from SMSs, like common words, words by SMS, the SMS is an spam or not, etc.
With this data the follow items will be shown.

- <a name=purpose_step_1></a>Step 1:
   - A word cloud graphic containing the most frequently words from the database.
   - A graphic containing the commons messages and spam message by month.
   - <a name="item_3_step_1"></a>The calculation of the maximum, minimum, average, median, standard deviation and variance of the total number of words.
   - <a name="item_4_step_1"></a>The day of each month that contains the largest sequence of common messages received (not spam).

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
   - Step 2: Classify the SMSs from the file `sms_database.csv` between common messages and spam messages, like [Step 2](#purpose_step_2) describes. This step uses the [Naive Bayes classifier](https://en.wikipedia.org/wiki/Naive_Bayes_classifier) to classify the SMSs. 

## Results

- Step 1:
   - For the first two items the results will be printed in graphics, in images stored in folder `./output/`.
      - `wordcloud.png`: This file shows the most repeated words in the messages, using a word cloud graphic.
      - `messages-by-month.png`: This file shows all the messages classified between spam and not spam by month.
   - For the last two items the results will be printed in console.
      - `Statistics by Month`: This item shows the result about the item [three](#item_3_step_1) in step 1. Is printed the max, min, average, median, standard deviation and variance.
      - `Day of the Month with more Common Messages`: This item prints the day of each month that contains the biggest number of common messages, like described in item [four](#item_4_step_1).

- Step 2:
   - The results will be printed in console and the files `output.csv` and `output-difference.csv` will be create in folder `./output/`. The two files has 3 columns
      - Column: `IsSpam`: This column contain the original data from database if the message is a spam or common message.
      - Column: `IsSpam-Prediction`: This column contain the information calculate by Naive Bayes classifier if the message is a spam or common message.
      - Column: `Full_Text`: This column contain the messages from the original database.
   - File `output.csv`
      - This file contains all messages from the database. Is a CSV file with 3 columns.
   - File `output-difference.csv`
      - This file contains only the messages that the Naive Bayes classifier misclassified. That is, only the records with the `IsSpam` and `IsSpam-Prediction` columns that have different values.