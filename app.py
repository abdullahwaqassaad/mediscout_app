import streamlit as st
import pandas as pd
import os

# --- Existing data load ---
# df = pd.read_csv('your_data.csv')  # your data file

# --- Input on main page ---
st.header("Enter your symptom or keyword")
user_input = st.text_input("Keyword:")

if st.button("Save Input") and user_input:
    # Save to CSV
    if os.path.exists('user_data.csv'):
        df_user = pd.read_csv('user_data.csv')
    else:
        df_user = pd.DataFrame(columns=['symptom'])
    df_user = df_user.append({'symptom': user_input}, ignore_index=True)
    df_user.to_csv('user_data.csv', index=False)
    st.success("Input saved!")

# --- Filter your data ---
if user_input:
    filtered_df = df[df['symptoms'].str.contains(user_input, case=False, na=False)]
else:
    filtered_df = df

# --- Continue with your existing features like maps, graphs, tables ---
st.write("Filtered Data:")
st.dataframe(filtered_df)

# Your map or other visualization code here
