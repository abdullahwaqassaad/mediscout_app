import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("MediScout Pakistan Prototype")

# Sample dataset with age and gender
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
    'disease_flag': [1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
    'age': [25, 30, 45, 22, 60, 35, 40, 50, 29, 33],  # Age data
    'gender': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female']
}

df = pd.DataFrame(data)

# Filters
selected_symptom = st.selectbox("Select Symptom", df['symptoms'].unique())

# Additional filters for age and gender
age_range = st.slider("Select Age Range", min_value=int(df['age'].min()), max_value=int(df['age'].max()), value=(20, 60))
selected_gender = st.selectbox("Select Gender", ['All'] + list(df['gender'].unique()))

# Apply filters
filtered_df = df[df['symptoms'] == selected_symptom]
filtered_df = filtered_df[
    (filtered_df['age'] >= age_range[0]) & (filtered_df['age'] <= age_range[1])
]
if selected_gender != 'All':
    filtered_df = filtered_df[filtered_df['gender'] == selected_gender]

# Show data
st.write("Filtered Data:", filtered_df)

# Map
st.map(filtered_df[['lat', 'lon']])

# Plot: Count of diseases in filtered data
st.header("Disease Counts")
disease_counts = filtered_df['diseases'].value_counts()
fig, ax = plt.subplots()
disease_counts.plot.bar(ax=ax)
ax.set_xlabel("Disease")
ax.set_ylabel("Count")
st.pyplot(fig)
