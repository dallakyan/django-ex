from textstat.textstat import textstat
from textblob import TextBlob


#Using this method to import all the Text Analysis that
#is carried out in each of the API search engines
def text_analysis(x):
    for result in x:
        blob = TextBlob(result['summary'])
        for text in blob.sentences:
            result['pola'] = '%.2f' % (abs(text.sentiment.polarity*10)/2) #-1 to 1
            result['subj'] = '%.2f' % (abs(text.sentiment.subjectivity*10)/2) #-1 to 1
            result['reada'] = '%.2f' % textstat.flesch_kincaid_grade(result['summary'])   #out of 10
    return x

