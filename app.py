import streamlit as st
import pandas as pd
import os

# Load data
@st.cache
def load_data():
    return pd.read_csv('test_data.csv')

df = load_data()

st.header("Search Symptoms or Keywords")
user_input = st.text_input("Enter symptom or keyword:")

if st.button("Save Input") and user_input:
    save_path = 'user_data.csv'
    if os.path.exists(save_path):
        df_user = pd.read_csv(save_path)
    else:
        df_user = pd.DataFrame(columns=['symptom'])
    df_user = df_user.append({'symptom': user_input}, ignore_index=True)
    df_user.to_csv(save_path, index=False)
    st.success("Your input has been saved!")

if user_input:
    filtered_df = df[df['symptoms'].str.contains(user_input, case=False, na=False)]
else:
    filtered_df = df

st.subheader("Filtered Data")
st.dataframe(filtered_df)
