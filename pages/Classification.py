import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from collections import defaultdict
import warnings
warnings.filterwarnings(action='ignore', category=FutureWarning)
from models_features import models_features as mf
import pickle

st.set_page_config(
    page_title="Classification Prediction"
)

st.title("Classification Prediction")
st.header("Wash Item Prediction")

df = pd.read_csv("processed_data.csv")

st.subheader("Please enter selections: ")

mfObj = mf()
Y_Cols = mfObj.classification_feature_cols
x_col = mfObj.classification_target
label_Cols = mfObj.label_encoding_columns

resInput = dict()

for col in Y_Cols:
    if col == "DayOfWeek":
        resInput[col] = st.selectbox(col + ": ", df[col].unique(), 
        format_func=lambda x : ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][x])
    elif col in label_Cols:
        resInput[col] = st.selectbox(col + ": ", df[col].unique())
    elif col == "HourInDay":
        resInput[col] = st.selectbox(col + ": ", list(range(23)))
    else:
        resInput[col] = st.number_input(col, min_value=0) 

if st.button('Predict'):
    resDF = pd.DataFrame(resInput, index=[0])

    for col in Y_Cols:
        if not col in label_Cols:
            continue

        pkl_file = open(f"deployment/encoders/{col}_encoder.pkl", "rb")
        label_encoder = pickle.load(pkl_file)
        pkl_file.close()
        resDF[col] = label_encoder.transform(resDF[col])
    

    pkl_file = open(f"deployment/models/nb_classifier.pkl", "rb")
    model = pickle.load(pkl_file)
    pkl_file.close()
    
    Y = model.predict(resDF)

    pkl_file = open(f"deployment/encoders/{x_col}_encoder.pkl", "rb")
    label_encoder = pickle.load(pkl_file)
    pkl_file.close()

    YVal = label_encoder.inverse_transform(Y)[0]
    
    st.write("The predicted value is " + YVal)





    