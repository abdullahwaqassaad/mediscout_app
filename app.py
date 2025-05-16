import streamlit as st  
import pandas as pd  
import os  
import matplotlib.pyplot as plt  

st.title("MediScout Pakistan Prototype")  

# --- Your existing dataset ---  
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
    'age': [25, 30, 45, 22, 60, 35, 40, 50, 29, 33],  
    'gender': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female']  
}  
df = pd.DataFrame(data)  

# --- Sidebar: Add new patient data with a form ---  
st.sidebar.header("Register New Patient")  
with st.sidebar.form(key='patient_form'):  
    name = st.text_input("Name")  
    age = st.number_input("Age", min_value=0, max_value=120)  
    gender = st.selectbox("Gender", ['Male', 'Female', 'Other'])  
    symptoms_input = st.text_input("Symptoms (comma separated)")  
    disease_input = st.text_input("Disease")  
    submit_button = st.form_submit_button("Add Patient Data")  

# --- Handle form submission ---  
if submit_button:  
    patient_data_path = 'patients.csv'  
    if os.path.exists(patient_data_path):  
        patients_df = pd.read_csv(patient_data_path)  
    else:  
        patients_df = pd.DataFrame(columns=['name', 'age', 'gender', 'symptoms', 'disease'])  

    new_patient = {  
        'name': name,  
        'age': age,  
        'gender': gender,  
        'symptoms': symptoms_input,  
        'disease': disease_input  
    }  
    patients_df = patients_df.append(new_patient, ignore_index=True)  
    patients_df.to_csv(patient_data_path, index=False)  
    st.sidebar.success(f"Patient {name} data added!")  
    st.write(f"Patient {name} data saved!")  # debugging info  

# --- Filters ---  
selected_symptom = st.selectbox("Select Symptom", df['symptoms'].unique())  
age_min, age_max = int(df['age'].min()), int(df['age'].max())  
age_range = st.slider("Select Age Range", min_value=age_min, max_value=age_max, value=(age_min, age_max))  
selected_gender = st.selectbox("Select Gender", ['All'] + list(df['gender'].unique()))  

# --- Apply filters ---  
filtered_df = df[df['symptoms'] == selected_symptom]  
filtered_df = filtered_df[  
    (filtered_df['age'] >= age_range[0]) & (filtered_df['age'] <= age_range[1])  
]  
if selected_gender != 'All':  
    filtered_df = filtered_df[filtered_df['gender'] == selected_gender]  

# --- Show filtered data ---  
st.write("Filtered Data:", filtered_df)  

# --- Map ---  
st.map(filtered_df[['lat', 'lon']])  

# --- Plot disease counts if there are results ---  
st.header("Disease Counts")  
if not filtered_df.empty:
    fig, ax = plt.subplots()
    filtered_df['diseases'].value_counts().plot.bar(ax=ax)
    ax.set_xlabel("Disease")
    ax.set_ylabel("Count")
    st.pyplot(fig)
else:
    st.write("No data to display for the selected filters.")
