from SMSClassifier import SMSClassifier
from SMSStatistics import SMSStatistics

def smsStatistics():
    return SMSStatistics()

def smsClassifier():
    return SMSClassifier()

options = {1: smsStatistics, 2: smsClassifier}

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def main():
  print('Select the step desired\n(1): SMS Statistics\n(2): SMS Classifier\n(0): Quit')
  step = input('Select the step desired:\n')

  if (isNumber(step) and int(step) >= 0 and int(step) < 3):
      options.get(int(step))().run()
  else:
    print('Please inform a valid number')
    main()

main()