import streamlit as st
from model import load_model,randomSampleW
from preprocess import word_tag_idx

@st.cache_resource  
def Loading_Model():
    model = load_model()
    word2idx,idx2word,tag2idx,idx2tag = word_tag_idx()
    return model, word2idx,idx2word,tag2idx,idx2tag 

model,word2idx,idx2word,tag2idx,idx2tag = Loading_Model()

st.title("DEMO")
st.subheader("**INPUT**:")
text_input = st.text_area(" ",height = 15)
outputs = randomSampleW(text_input,model,word2idx,idx2tag,1)
st.subheader("**OUTPUT**:")
for output in outputs:
    st.text(output)
    

