import streamlit as st
import pandas as pd

st.title("MediScout Pakistan Prototype")

# Example dataset
data = {
    'id': [1, 2, 3],
    'symptoms': ['Fever', 'Cough', 'Headache'],
    'lat': [25.0, 24.8, 24.9],
    'lon': [67.0, 67.2, 67.1],
    'disease_flag': [1, 0, 1]
}
df = pd.DataFrame(data)

# Dropdown to select symptoms
symptom = st.selectbox("Select Symptom", df['symptoms'].unique())

# Filter data
filtered_df = df[df['symptoms'] == symptom]

# Show filtered data
st.write("Filtered Data:", filtered_df)
