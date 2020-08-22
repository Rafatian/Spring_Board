import time
import numpy as np
import nltk
from nltk.stem import PorterStemmer
import re
import pickle
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from PIL import Image
import tensorflow.keras.models as models
import streamlit as st

#Creating a function to clean text and git rid of punctuations, stopwords, and lowering the text
wpt = nltk.WordPunctTokenizer()
stop_words = nltk.corpus.stopwords.words('english')
ps = PorterStemmer()

def normalize_document(doc):
    # lower case and remove special characters\whitespaces
    doc = re.sub(r'[^a-zA-Z\s]', '', doc, re.I|re.A)
    doc = doc.lower()
    doc = doc.strip()
    # tokenize document
    tokens = wpt.tokenize(doc)
    # filter stopwords and non english words out of document
    filtered_tokens = [token for token in tokens if token not in stop_words]
    # re-create document from filtered tokens
    stem_tokens = [ps.stem(word) for word in filtered_tokens]
    doc = ' '.join(stem_tokens)
    return doc

# loading
with open('tokenizer_text.pickle', 'rb') as handle:
    tokenizer_text = pickle.load(handle)

def text_tokenizer(news):
    sequences = tokenizer_text.texts_to_sequences(news)
    data = pad_sequences(sequences, maxlen=8502)
    return(data)

# loading
with open('tokenizer_title.pickle', 'rb') as handle:
    tokenizer_title = pickle.load(handle)

def title_tokenizer(title):
    sequences = tokenizer_title.texts_to_sequences(news)
    data = pad_sequences(sequences, maxlen=29)
    return(data)


model_text =Sequential()
model_text.add(layers.Embedding(20000, 100, input_length=8502))
model_text.add(layers.LSTM(32))
model_text.add(layers.Dropout(0.5))
model_text.add(layers.Dense(1, activation='sigmoid'))

model_text.load_weights('model_text.h5')
model_text.compile(optimizer='rmsprop', loss='binary_crossentropy',metrics=['acc'])


model_title =Sequential()
model_title.add(layers.Embedding(20000, 100, input_length=29))
model_title.add(layers.LSTM(32))
model_title.add(layers.Dropout(0.5))
model_title.add(layers.Dense(1, activation='sigmoid'))

model_title.load_weights('model_title.h5')
model_title.compile(optimizer='rmsprop', loss='binary_crossentropy',metrics=['acc'])

def news_predict(news):
    
    if news:
        doc = normalize_document(news)
        data = text_tokenizer(np.array([doc]))
        prediction = model_text.predict(data)
    
        return(prediction[0][0])

    else:
        print('No News Were Entered')

def title_predict(title):
    
    if news:
        doc = normalize_document(news)
        data = title_tokenizer(np.array([doc]))
        prediction = model_title.predict(data)
    
        return(prediction[0][0])

    else:
        print('No title Were Entered')


def main():

    st.markdown("<h1 style='text-align: center; color: black;'>FAKE NEWS ANALYSIS</h1>", unsafe_allow_html=True)
    img = Image.open('Newspaper.jpg')
    st.image(img,width=700)
    st.header("This API is developed to predict if a news article is Fake or True")
    st.text("The LSTM model behind this app has been trained on more than forty thousand news articles\nand has been able to predict the validity of an article with 99% accuracy")
    
    

    news = st.text_area("Please enter your article below:", "Paste News Here")
   
    if st.button("Analyze"):
        with st.spinner("Analyzing.."):
            time.sleep(2)
        prediction = news_predict(news)
        
        if prediction<.5:
            st.success("The News You Entered Is {0:.2f}% True!".format((1-prediction)*100))
        else:
            st.error("The News You Entered Is {0:.2f}%  False!".format(prediction*100))

    st.sidebar.header("Developer: Amin Rafatian")
    st.sidebar.text("""
    Data scientist with a strong background
    in Python and R programming.
    He has performed data cleaning, 
    wrangling,and statistical analysis on
    numerous datasets.He has created
    various predictive models using machine
    learning algorithms and produced
    analytical reports with meaningful data 
    visualizations. """)


if __name__ == '__main__':
    main()
    