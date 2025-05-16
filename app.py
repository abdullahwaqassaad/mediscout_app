import streamlit as st
import pandas as pd
import os

# --- Load your main dataset ---
# Replace 'your_data.csv' with your actual data file path
@st.cache
def load_data():
    return pd.read_csv('your_data.csv')

df = load_data()

# --- User input section ---
st.header("Search Symptoms or Keywords")
user_input = st.text_input("Enter symptom or keyword:")

# Save button
if st.button("Save Input") and user_input:
    # Save user input to CSV
    save_path = 'user_data.csv'
    if os.path.exists(save_path):
        df_user = pd.read_csv(save_path)
    else:
        df_user = pd.DataFrame(columns=['symptom'])
    df_user = df_user.append({'symptom': user_input}, ignore_index=True)
    df_user.to_csv(save_path, index=False)
    st.success("Your input has been saved!")

# --- Filter data based on user input ---
if user_input:
    # Assuming your dataset has a column named 'symptoms'
    filtered_df = df[df['symptoms'].str.contains(user_input, case=False, na=False)]
else:
    filtered_df = df

# --- Display filtered data ---
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# --- Continue with your map, graph, or other visualizations ---
# Example: Map or other visualizations using 'filtered_df'
# st.map(filtered_df[['latitude', 'longitude']]) # Example if coordinates are available
