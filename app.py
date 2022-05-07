from flask import Flask,render_template,url_for,request
from flask import jsonify
import pandas as pd 
import pickle
import re
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.layers import Embedding
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
import numpy as np
from flask_cors import CORS

import nltk
import re
from nltk.corpus import stopwords
voc_size=5000
from nltk.stem.porter import PorterStemmer
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()


app = Flask(__name__)
CORS(app)

def init():
    global model, embedded_docs_text, embedded_docs_aspect
    model=tf.keras.models.load_model(r"C:\Users\sameer\Desktop\sameer\backend\My_model1.h5")
    #embedded_docs_text=pickle.load(open(r"C:\Users\sameer\Desktop\Enterpret Project NLP\Enterpret Project\embedded_text.pickle","rb"))
    #embedded_docs_aspect=pickle.load(open(r"C:\Users\sameer\Desktop\Enterpret Project NLP\Enterpret Project\embedded_aspect.pickle","rb"))



    


@application.route('/predict', methods=['POST'])
def predict():
    JSONresponse = {}
    print('running444 ...')

    if request.method=='POST':
        contentType = request.headers.get('Content-Type')

        if contentType == 'application/json':
            json = request.json
            print(json)
        print('running ...')
        text = json.get('text')
        
        text = re.sub('[^a-zA-Z]',' ',str(text))
        text=text.lower()
        text=text.split()
        text=[ps.stem(word) for word in text if not word in stopwords.words('english')]
        text=' '.join(text)

        onehot_repr=[one_hot(words,voc_size)for words in [text]]
        sent_length=30
        embedded_docs_text=pad_sequences(onehot_repr,padding='pre',maxlen=sent_length)

         #repeat same with aspect
        aspect = json.get('aspect')
        aspect=re.sub('[^a-zA-Z]',' ',str(aspect))
        aspect=aspect.lower()
        aspect=text.split()
        aspect=[ps.stem(word) for word in aspect if not word in stopwords.words('english')]
        aspect=' '.join(aspect)

        onehot_repr1=[one_hot(words,voc_size)for words in [aspect]]
        sent_length1=30
        embedded_docs_aspect=pad_sequences(onehot_repr1,padding='pre',maxlen=sent_length1)
        a=embedded_docs_text
        b=embedded_docs_aspect
        #print('lrm :',len(a),len(b))
        
        pred = np.array(np.concatenate([a,b],axis=0)).reshape(1,-1)
        print('out ',len(pred))
        yPred = model.predict(pred)
        my_prediction1=np.argmax(yPred,axis=1)

        print(my_prediction1)
        
        if my_prediction1==0:
            JSONresponse['code'] = -1 
            JSONresponse['summary'] = 'The sentiment is negative'
        
        elif my_prediction1==1:
            JSONresponse['code'] = 0
            JSONresponse['summary'] = 'The sentiment is neutral'
        
        else:
            JSONresponse['code'] = 1
            JSONresponse['summary'] = 'The sentiment is positive'
    
    return jsonify(JSONresponse)

if __name__=='__main__':
    init()
    application.run()
        
        
    
