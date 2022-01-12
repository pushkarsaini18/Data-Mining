#!/usr/bin/env python
# coding: utf-8

# #### Import Necessary Library

# In[1]:


import requests                  #Requests will allow you to send HTTP/1.1 requests using Python
import pandas as pd              #Python package providing fast, flexible, and expressive data structures
from bs4 import BeautifulSoup    #for web scraping purposes to pull the data out of HTML and XML files
from textblob import TextBlob    #for processing textual data
import textstat                  # to calculate statistics from. # text
import openpyxl                 #a Python library for reading and writing Excel
import string                  #contains a number of functions to process standard Python strings,
import spacy                  #for “Industrial strength NLP in Python
import re                      #provides full support for Perl-like regular expressions


# #### Import NLTK for tokenizing, Tagging, stopwords

# In[119]:


import nltk                 #toolkit build for working with NLP in Python eg: tokenizing, Tagging, stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')


# #### Positive & Negative words dictionary 

# In[120]:


with open("G:/Data science/assignment/text minning(done)/negative-words.txt","r",encoding = "ISO-8859-1") as neg:
    negwords = neg.read().split("\n")


# In[121]:


with open("G:/Data science/assignment/text minning(done)/positive-words.txt","r") as pos:
    poswords = pos.read().split("\n") 


# #### Python program to fetch link and perform required operation

# In[124]:


import openpyxl

data=[]

def text(): 

    ######## for fetching data from given input excel sheet ########
    wb = openpyxl.load_workbook('Input.xlsx')  
    ws = wb['Sheet1']
    
    ####### fetch the url from sheet into url variable ############ 
    for i in range (2 , 172):
        url = (ws.cell(row=i, column=2).value)
    
    #We need to pass argument called Headers by passing "User-Agent" to the request to bypass the mod-security error.

        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}     
        page = requests.get(url, headers=headers)
    
    # apply BeautifulSoup to fetch only html parser 
        soup = BeautifulSoup(page.content, 'html.parser')
        
    # fetch title from link
        title = soup.find('h1',class_="entry-title").text.replace('\n'," ")
    
    #fetch content from link and remove unwanted header & punctuation
        content = soup.findAll(attrs={'class':'td-post-content'})    
        content = content[0].text.replace('\n'," ")    
        content = content.translate(str.maketrans('', '', string.punctuation)) 
    
    #tokenize the data 
        text_tokens = word_tokenize(content)
        
    
    #remove stopwords
        my_stop_words = stopwords.words('english')
        no_stop_tokens = [word for word in text_tokens if not word in my_stop_words]
    
    #count positive score usnig positive dictionary 
        pos_count = " ".join ([w for w in no_stop_tokens if w in poswords])   
        pos_count=pos_count.split(" ")  
        Positive_score=len(pos_count)
    
    #count negative score usnig negative dictionary
        neg_count = " ".join ([w for w in no_stop_tokens if w in negwords])    
        neg_count=neg_count.split(" ")    
        Negative_score=len(neg_count)
        
    #join filter data after removing stpowords  
        filter_content = ' '.join(no_stop_tokens)
        
    #words count 
        Word_Count=len(content)
        
    #Avg_Sentence_Lenght count 
        Avg_Sentence_Lenght = len(content.replace(' ',''))/len(re.split(r'[?!.]', content))
    
    #calculating fog index using textstat library
        Fog_Index=(textstat.gunning_fog(content))
    
    #Avg_Number_of_Words_Per_Sentence count
        Avg_Number_of_Words_Per_Sentence = [len(l.split()) for l in re.split(r'[?!.]', content) if l.strip()]
        Avg_Number_of_Words_Per_Sentence=(sum(Avg_Number_of_Words_Per_Sentence)/len(Avg_Number_of_Words_Per_Sentence))
    
        Word_Count=len(content)

        
    #function to calculate Complex_Words consedring word not ending from "ed" or "es"
        def syllablecount(word):
            coun = 0
            vowels = "AEIOUYaeiouy"
            if word[0] in vowels:
                coun = coun + 1
            for index in range(1, len(word)): 
                    if word[index] in vowels and word[index - 1] not in vowels:
                        coun = coun + 1
                        if word.endswith("es"or "ed"):
                            coun = coun - 1
            if coun == 0:
                coun = coun + 1
            return coun
        Complex_Words = syllablecount(content)

    
    #function to calculate proper noun in article with help of tagging from nltk lib
        def ProperNounExtractor(text):
            cou = 0
            sentences = nltk.sent_tokenize(text)
            for sentence in sentences:
                words = nltk.word_tokenize(sentence)
                tagged = nltk.pos_tag(words)
                for (word, tag) in tagged:
                    if tag == 'PRP': # If the word is a proper noun
                        cou = cou + 1 
        
            return(cou) 
        Personal_Pronouns=ProperNounExtractor(content)
    

    #function for sentiment analysis
        def sentiment_analysis(text):
            sentiment = TextBlob(text).sentiment
            return (sentiment.polarity)
    
        polarity=sentiment_analysis(content)
  
        def sentiment_analysis(text):
            sentiment = TextBlob(text).sentiment
            return (sentiment.subjectivity)
    
        subjectivity=sentiment_analysis(content)
        
        
    #method to count average syllable count in words
        word=content.replace(' ','')
        syllable_count = 0
        for w in word:
            
            if(w=='a' or w=='e' or w=='i' or w=='o' or w=='y' or w=='u' or w=='A' or w=='E' or w=='I' or w=='O' or w=='U' or w=='Y'):
                syllable_count=syllable_count+1

        Syllable_Per_Word=(syllable_count/len(content.split()))
        
    # calculate average word lenght 
        Average_Word_Length=len(content.replace(' ',''))/len(content.split())
        
    # calculate % of complex word
        Percentage_of_Complex_Word = Complex_Words / Word_Count * 100
    
        data.insert(i,[url,Positive_score, Negative_score, polarity,subjectivity, Avg_Sentence_Lenght,Percentage_of_Complex_Word,Fog_Index, Avg_Number_of_Words_Per_Sentence , Complex_Words, Word_Count,Syllable_Per_Word, Personal_Pronouns, Average_Word_Length])
        

    
if __name__ == '__main__' :  
    text()
        
df = pd.DataFrame(data,columns=['url','Positive_score','Negative_score','polarity','subjectivity', 'Avg_Sentence_Lenght','Percentage_of_Complex_Word', 'Fog_Index', 'Avg_Number_of_Words_Per_Sentence' , 'Complex_Words', 'Word_Count', 'Syllable_Per_Word','Personal_Pronouns', 'Average_Word_Length'])


# In[125]:


df.to_csv('linkd.csv')
df


# In[ ]:




