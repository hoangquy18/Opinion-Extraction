from CRF_Layer import CRF
from keras.initializers import Constant
from keras.layers import Dense,Input,GlobalAveragePooling1D ,concatenate,Dropout,GRU,Bidirectional,TimeDistributed, Embedding, Attention, LSTM,Convolution1D,MaxPooling1D,Flatten,SpatialDropout1D,LeakyReLU,AveragePooling1D,MultiHeadAttention,GlobalMaxPooling1D,Dropout
from keras.models import Model
from keras.optimizers import Adamax,Adam
from keras.losses import CategoricalCrossentropy,BinaryCrossentropy
from keras.regularizers import L1,L2
from keras.initializers import Orthogonal
from keras.callbacks import EarlyStopping
from preprocess import Preprocessing,word_tag_idx
import numpy as np
from keras.utils import pad_sequences
import re

MAX_LEN = 60
def load_model():
    input = Input(shape=(MAX_LEN,))
    embedding = Embedding(input_dim= 979460, output_dim=100, 
                    input_length=MAX_LEN, )(input)  
    bi_lstm = Bidirectional(LSTM(units=100, return_sequences=True,
                            recurrent_dropout=0.1))(embedding) 

    time = TimeDistributed(Dense(92, activation="softmax"))(bi_lstm) 

    crf = CRF(92)  
    output = crf(time)

    w_model = Model(input,output)
    w_model.compile(optimizer=Adamax(learning_rate = 0.005),loss = CRF.loss)
    w_model.load_weights("w_weights_last.h5")
    return w_model

def randomSampleW(text,model,word2idx,idx2tag,printed = False,):
  text = Preprocessing().TextNormalized(text)
  text = text.lower()

  text_encoded = []
  for word in text.split():
    try:
      text_encoded.append(word2idx[word])
    except:
      text_encoded.append(word2idx["UNK"])

  text_encoded = pad_sequences(np.array([text_encoded]),maxlen=MAX_LEN,padding='post',truncating = 'post',value = word2idx['PAD'])

  y_pred = np.argmax(model.predict([text_encoded],verbose = 0),axis = -1)
  y_s = list(map(lambda x:idx2tag[x],y_pred[0]))
  ydx = []
  output = []
  pt = ""
  for i in range(len(y_s)):
    if "B-" in y_s[i] :
        ydx.append(i)
  print(ydx)

  if printed:
    text = text.split()
    if len(ydx) == 0:
      return " "    
    if len(ydx) == 1:
        pt+= " ".join(text) + ": "+y_s[ydx[0]][2:]
        output.append(pt)
        return output
    for i in range(len(ydx)-1):
        start = ydx[i]
        end = ydx[i+1] - 1
        pt = ""
        for j in range(start,end):
            pt += text[j] + " "
        pt += ": " + y_s[ydx[i]][2:]
        output.append(pt)
    
    f = ydx[-1]
    pt = ""
    for i in range(f,len(text)):
        if "I-" in y_s[i] or "B-" in y_s[i]:
            pt += text[i] + " "
    pt += ": " + y_s[ydx[-1]][2:]
    output.append(pt)
    # for k,v in zip(text.split(),y_pred[0]):
    #   print(k,idx2tag[v])
  return output