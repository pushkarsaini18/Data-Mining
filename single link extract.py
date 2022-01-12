#!/usr/bin/env python
# coding: utf-8

# ## Import Library

# In[1]:


import requests
import pandas as pd 
from bs4 import BeautifulSoup
import string
import spacy
import re


# ### Text Analysis (1 url)
# 
# #### Scrap Data

# In[2]:


url="""https://insights.blackcoffer.com/how-is-login-logout-time-tracking-for-employees-in-office-done-by-ai/"""


# In[3]:


headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')


# We need to pass argument called Headers by passing "User-Agent" to the request to bypass the mod-security error.

# In[4]:


soup=BeautifulSoup(page.content, 'html.parser')
soup


# #### Extract Title from articel

# In[5]:


title=soup.find('h1',class_="entry-title")
title=title.text.replace('\n'," ")
title


# #### Extract Content from articel

# In[6]:


content=soup.findAll(attrs={'class':'td-post-content'})
content=content[0].text.replace('\n'," ")
content


# #### Remove punctuation from the content

# In[7]:


#Punctuation
content = content.translate(str.maketrans('', '', string.punctuation)) 
content


# #### convert into Tokens 

# In[9]:


#Tokenization
from nltk.tokenize import word_tokenize
text_tokens = word_tokenize(content)
print(text_tokens[0:50])


# ####  lenghts of tokens before removing stopwords

# In[10]:


len(text_tokens)


# #### Remove stopwords from the tokens

# In[11]:


#Remove stopwords
import nltk
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

my_stop_words = stopwords.words('english')
my_stop_words.append('the')
no_stop_tokens = [word for word in text_tokens if not word in my_stop_words]
print(no_stop_tokens[0:40])


# ####  lenghts of tokens after removing stopwords

# In[12]:


len(no_stop_tokens)


# #### Check for positive words

# In[13]:


with open("G:/Data science/assignment/text minning(done)/positive-words.txt","r") as pos:
    poswords = pos.read().split("\n")  
    poswords = poswords[5:]


# Download the positive words dictionary and store in local system to speed up the process

# In[14]:


pos_count = " ".join ([w for w in no_stop_tokens if w in poswords])
pos_count=pos_count.split(" ")


# #### Positive Score

# In[15]:


Positive_score=len(pos_count)
print(Positive_score)


# #### Check for negative words

# In[16]:


with open("G:/Data science/assignment/text minning(done)/negative-words.txt","r",encoding = "ISO-8859-1") as neg:
    negwords = neg.read().split("\n")
    
negwords = negwords[36:]


# In[17]:


neg_count = " ".join ([w for w in no_stop_tokens if w in negwords])
neg_count=neg_count.split(" ")


# #### Negative score

# In[18]:


Negative_score=len(neg_count)
print(Negative_score)


# In[19]:


filter_content = ' '.join(no_stop_tokens)


# In[20]:


data=[[url,title,content,filter_content,Positive_score,Negative_score]]


# In[21]:


data=pd.DataFrame(data,columns=["url","title","content","filter_content","Positive_Score","Negative_Score"])


# #### calculate Polarity Score & Subjectivity Score

# In[22]:


from textblob import TextBlob

# Get The Subjectivity
def sentiment_analysis(data):
    sentiment = TextBlob(data["content"]).sentiment
    return pd.Series([sentiment.polarity,sentiment.subjectivity ])

# Adding Subjectivity & Polarity
data[["polarity", "subjectivity"]] = data.apply(sentiment_analysis, axis=1)

data


# #### Average sentence length

# In[23]:


#AVG SENTENCE LENGTH
AVG_SENTENCE_LENGTH = len(content.replace(' ',''))/len(re.split(r'[?!.]', content))
print('Word average =', AVG_SENTENCE_LENGTH)


# In[24]:


import textstat


# Textstat is an easy to use library to calculate statistics from text. It helps determine readability, complexity, and grade level.

# #### FOG INDEX

# In[25]:


FOG_INDEX=(textstat.gunning_fog(content))
print(FOG_INDEX)


# #### AVG NUMBER OF WORDS PER SENTENCE

# In[38]:


AVG_NUMBER_OF_WORDS_PER_SENTENCE = [len(l.split()) for l in re.split(r'[?!.]', content) if l.strip()]
print(sum(AVG_NUMBER_OF_WORDS_PER_SENTENCE)/len(AVG_NUMBER_OF_WORDS_PER_SENTENCE))


# #### COMPLEX WORD COUNT

# In[27]:


def syllable_count(word):
    count = 0
    vowels = "AEIOUYaeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)): 
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
            if word.endswith("es"or "ed"):
                count -= 1
    if count == 0:
        count += 1
    return count



COMPLEX_WORDS=syllable_count(filter_content)

print(COMPLEX_WORDS)


# #### Word Count

# In[28]:


Word_Count=len(filter_content)
print(Word_Count)


# #### Percentage of Complex words 

# In[67]:


pcw=(COMPLEX_WORDS/Word_Count)*100
print(pcw)


# #### Personal Pronouns

# In[61]:


def ProperNounExtractor(text):
    count = 0
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(words)
        for (word, tag) in tagged:
            if tag == 'PRP': # If the word is a proper noun
                count = count + 1 
        
    return(count)         
                


# Calling the ProperNounExtractor function to extract all the proper nouns from the given text. 
Personal_Pronouns=ProperNounExtractor(content)  


# #### Average Word Length

# In[34]:


Average_Word_Length=len(content.replace(' ',''))/len(content.split())
print(AWL)


# In[47]:


data


# In[66]:


data=[[url,title,content,filter_content,Positive_Score,Negative_Score,polarity,subjectivity,AVG_SENTENCE_LENGTH,FOG_INDEX,AVG_NUMBER_OF_WORDS_PER_SENTENCE,COMPLEX_WORDS,Word_Count,Average ]]


# In[ ]:




