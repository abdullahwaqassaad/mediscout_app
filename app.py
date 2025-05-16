import streamlit as st
import pandas as pd

st.title("MediScout Pakistan Prototype")

# Expanded dataset with 10 symptoms and diseases
data = {
    'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'symptoms': [
        'Fever', 'Cough', 'Headache', 'Sore Throat', 'Nausea',
        'Fatigue', 'Shortness of Breath', 'Muscle Pain', 'Dizziness', 'Runny Nose'
    ],
    'diseases': [
        'Malaria', 'Flu', 'Migraine', 'Pharyngitis', 'Gastroenteritis',
        'Anemia', 'Asthma', 'Influenza', 'Vertigo', 'Common Cold'
    ],
    'lat': [25.0, 24.8, 25.2, 24.9, 25.1, 24.7, 25.3, 24.9, 25.0, 24.8],
    'lon': [67.0, 67.2, 67.1, 67.3, 67.4, 67.2, 67.1, 67.3, 67.2, 67.4],
    'disease_flag': [1, 1, 1, 1, 1, 0, 0, 1, 0, 0]
}

df = pd.DataFrame(data)

# Unique options for filtering
symptom_options = df['symptoms'].unique()
disease_options = df['diseases'].unique()

# User selections
selected_symptom = st.selectbox("Select Symptom", symptom_options)
selected_disease = st.selectbox("Select Disease", disease_options)

# Filter data based on selections
filtered_df = df[
    (df['symptoms'] == selected_symptom) &
    (df['diseases'] == selected_disease)
]

# Show filtered data
st.write("Filtered Data:", filtered_df)

# Show locations on a map
st.map(filtered_df[['lat', 'lon']])
