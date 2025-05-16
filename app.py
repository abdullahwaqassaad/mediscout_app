import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.title("MediScout Pakistan Prototype")

# --- Your sample dataset ---
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

# --- Add new data feature in the sidebar ---
st.sidebar.header("Add New Symptom or Disease")
new_symptom = st.sidebar.text_input("New Symptom")
new_disease = st.sidebar.text_input("Associated Disease")
# You can add more fields as needed

if st.sidebar.button("Save New Data"):
    # Save to a CSV or append to your data
    save_path = 'your_data.csv'  # replace or set your data path
    if os.path.exists(save_path):
        df_existing = pd.read_csv(save_path)
    else:
        # Simulate existing dataframe structure if file doesn't exist
        df_existing = df.copy()

    # Append new data as a new row
    new_row = {
        'id': df_existing['id'].max() + 1,
        'symptoms': new_symptom,
        'diseases': new_disease,
        'lat': 25.0,  # default or user input
        'lon': 67.0,  # default or user input
        'disease_flag': 0,
        'age': 30,    # default or user input
        'gender': 'Male'  # default or user input
    }
    df_existing = df_existing.append(new_row, ignore_index=True)
    df_existing.to_csv(save_path, index=False)
    st.sidebar.success("New symptom/disease data saved!")

# --- Filters ---
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

# Show filtered data
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
