import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# ---- CONFIG ----
st.set_page_config(page_title="MediScout Pakistan", layout="wide")
USERS_FILE = 'users.csv'
PATIENT_FILE = 'patients.csv'

# ---- SESSION STATE ----
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'show_form' not in st.session_state:
    st.session_state.show_form = False

# ---- USER MANAGEMENT FUNCTIONS ----
def load_users():
    if os.path.exists(USERS_FILE):
        try:
            df = pd.read_csv(USERS_FILE)
            # Ensure required columns
            if 'username' not in df.columns or 'password' not in df.columns:
                return pd.DataFrame(columns=['username', 'password'])
            return df
        except Exception as e:
            st.error(f"Error loading users file: {e}")
            return pd.DataFrame(columns=['username', 'password'])
    else:
        return pd.DataFrame(columns=['username', 'password'])

def save_user(username, password):
    users_df = load_users()
    if username in users_df['username'].values:
        return False
    new_user = pd.DataFrame([{'username': username, 'password': password}])
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    users_df.to_csv(USERS_FILE, index=False)
    return True

def authenticate(username, password):
    users_df = load_users()
    return not users_df[(users_df['username'] == username) & (users_df['password'] == password)].empty

# ---- LOGIN / SIGNUP ----
if not st.session_state.logged_in:
    st.sidebar.title("Login / Signup")
    choice = st.sidebar.radio("Choose Option", ['Login', 'Signup'])

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if choice == 'Login':
        if st.sidebar.button("Login"):
            try:
                if username.strip() == "" or password.strip() == "":
                    st.sidebar.error("Please enter both username and password.")
                elif authenticate(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.experimental_rerun()  # triggers app rerun after login
                else:
                    st.sidebar.error("Invalid username or password.")
            except Exception as e:
                st.sidebar.error(f"Unexpected error during login: {e}")

    else:  # Signup
        if st.sidebar.button("Signup"):
            if username.strip() == "" or password.strip() == "":
                st.sidebar.error("Please enter both username and password.")
            elif save_user(username, password):
                st.sidebar.success("Signup successful. Please login.")
            else:
                st.sidebar.error("Username already exists.")
    st.stop()

# ---- LOGGED IN USER ----
st.sidebar.success(f"Welcome, {st.session_state.username}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.experimental_rerun()

# ---- PATIENT DATA HANDLING ----
def load_patients():
    if os.path.exists(PATIENT_FILE):
        return pd.read_csv(PATIENT_FILE)
    else:
        return pd.DataFrame(columns=['name', 'age', 'gender', 'symptoms', 'disease'])

def save_patient(new_patient):
    df = load_patients()
    new_df = pd.DataFrame([new_patient])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(PATIENT_FILE, index=False)

# ---- MAIN UI ----
st.title("🧠 MediScout Pakistan Prototype")

# ---- Toggle Register Form ----
if st.button("➕ Register New Patient"):
    st.session_state.show_form = not st.session_state.show_form

# ---- Register New Patient ----
if st.session_state.show_form:
    with st.form("patient_form"):
        st.subheader("Patient Registration Form")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120)
        gender = st.selectbox("Gender", ['Male', 'Female', 'Other'])
        symptoms = st.text_input("Symptoms (comma separated)")
        disease = st.text_input("Disease")
        submit = st.form_submit_button("Add Patient")

        if submit:
            save_patient({
                'name': name,
                'age': age,
                'gender': gender,
                'symptoms': symptoms,
                'disease': disease
            })
            st.success(f"Patient {name} added successfully!")

# ---- DELETE PATIENT ----
st.subheader("🗑️ Delete Patient Record")
del_name = st.text_input("Enter name to delete")
if st.button("Delete Patient"):
    df = load_patients()
    if del_name in df['name'].values:
        df = df[df['name'] != del_name]
        df.to_csv(PATIENT_FILE, index=False)
        st.success(f"Deleted {del_name}")
    else:
        st.warning("Name not found.")

# ---- SEARCH PATIENT ----
st.subheader("🔍 Search Patient")
search_name = st.text_input("Search by Name")
if st.button("Search"):
    df = load_patients()
    record = df[df['name'].str.lower() == search_name.lower()]
    if not record.empty:
        st.success("Patient Found:")
        st.dataframe(record)
    else:
        st.warning("No patient found.")

import random

# Load real patients instead of demo data
patients_df = load_patients()

# Only process if data exists
if not patients_df.empty:
    # Add missing fields for filtering and mapping
    if 'lat' not in patients_df.columns:
        patients_df['lat'] = [round(random.uniform(24.7, 25.3), 4) for _ in range(len(patients_df))]
    if 'lon' not in patients_df.columns:
        patients_df['lon'] = [round(random.uniform(67.0, 67.4), 4) for _ in range(len(patients_df))]
    if 'disease_flag' not in patients_df.columns:
        patients_df['disease_flag'] = patients_df['disease'].apply(lambda x: 1 if x else 0)

    # Rename for compatibility with filters
    patients_df.rename(columns={
        'symptoms': 'symptoms',
        'disease': 'diseases',
        'age': 'age',
        'gender': 'gender'
    }, inplace=True)

    df_demo = patients_df.copy()
else:
    st.warning("No patient data found. Please add some records.")
    df_demo = pd.DataFrame()

# ---- FILTERS ----
st.header("📊 Filter Disease Data")

# Load patient data
patients_df = load_patients()

if not patients_df.empty:
    # Ensure required columns exist
    required_cols = ['age', 'gender', 'symptoms', 'disease']
    for col in required_cols:
        if col not in patients_df.columns:
            patients_df[col] = ""

    # Add lat/lon if not exist (simulate for now)
    if 'lat' not in patients_df.columns:
        patients_df['lat'] = [round(random.uniform(24.7, 25.3), 4) for _ in range(len(patients_df))]
    if 'lon' not in patients_df.columns:
        patients_df['lon'] = [round(random.uniform(67.0, 67.4), 4) for _ in range(len(patients_df))]

    # Add disease_flag
    if 'disease_flag' not in patients_df.columns:
        patients_df['disease_flag'] = patients_df['disease'].apply(lambda x: 1 if pd.notna(x) and x.strip() != "" else 0)

    # Rename for compatibility
    patients_df.rename(columns={'disease': 'diseases'}, inplace=True)

    # Filters UI
    symptoms_unique = patients_df['symptoms'].dropna().unique()
    if len(symptoms_unique) == 0:
        st.info("No symptom data available.")
    else:
        selected_symptom = st.selectbox("Select Symptom", symptoms_unique)
        age_range = st.slider("Select Age Range", 1, 120, (1, 120))
        selected_gender = st.selectbox("Select Gender", ['Select'] + patients_df['gender'].dropna().unique().tolist())

        # Apply filters
        filtered_df = patients_df[patients_df['symptoms'] == selected_symptom]
        filtered_df = filtered_df[(filtered_df['age'] >= age_range[0]) & (filtered_df['age'] <= age_range[1])]
        if selected_gender != 'Select':
            filtered_df = filtered_df[filtered_df['gender'] == selected_gender]

        st.write("Filtered Data:", filtered_df)
        st.map(filtered_df[['lat', 'lon']])

        st.header("📈 Disease Counts")
        if not filtered_df.empty:
            fig, ax = plt.subplots()
            filtered_df['diseases'].value_counts().plot(kind='bar', ax=ax)
            ax.set_xlabel("Disease")
            ax.set_ylabel("Count")
            st.pyplot(fig)
        else:
            st.info("No data for selected filters.")
else:
    st.warning("No patient data available. Please add some records.")

# ---- Simulated Data Constants ----
SIM_FILE = 'simulated_data.csv'

def generate_simulated_data(days=45, records_per_day=20):
    simulated = []
    genders = ['Male', 'Female']
    
    for day_offset in range(days):
        date = (datetime.now() - timedelta(days=day_offset)).strftime('%Y-%m-%d')
        for _ in range(records_per_day):
            age = np.random.randint(0, 80)
            gender = np.random.choice(genders)
            temp = round(np.random.normal(37, 0.7), 1)

            disease = ""
            symptoms = []

            # Monsoon fever (25%)
            if np.random.rand() < 0.25:
                temp = round(np.random.uniform(38.0, 40.0), 1)
                disease = "Fever"
                symptoms = ["High Fever", "Body Aches", "Chills"]

            if age < 5:
                if np.random.rand() < 0.39:
                    disease = "Diarrhea"
                    symptoms = ["Loose stools", "Dehydration"]
                if np.random.rand() < 0.38:
                    disease = "Stunting"
                    symptoms.append("Poor Growth")
                if np.random.rand() < 0.177:
                    disease = "Wasting"
                    symptoms.append("Thin appearance")
                if np.random.rand() < 0.75:
                    disease = "ARI"
                    symptoms = ["Cough", "Difficulty Breathing", "Fever"]

            if np.random.rand() < 0.0026:
                disease = "TB"
                symptoms = ["Chronic Cough", "Weight Loss", "Fever"]

            if 18 <= age <= 40 and gender == 'Female' and np.random.rand() < 0.1:
                disease = "Pregnancy Complication"
                symptoms = ["Abdominal Pain", "Fever", "Vomiting"]

            if age >= 18 and np.random.rand() < 0.373:
                disease = "Hypertension"
                symptoms = ["High BP", "Headache"]

            if age >= 18 and np.random.rand() < 0.314:
                disease = "Diabetes"
                symptoms = ["Increased thirst", "Frequent urination"]

            immunized = "Yes" if age <= 2 and np.random.rand() < 0.66 else "No"

            simulated.append({
                "date": date,
                "name": f"SimUser_{np.random.randint(1000,9999)}",
                "age": age,
                "gender": gender,
                "temperature_C": temp,
                "symptoms": ", ".join(symptoms),
                "disease": disease,
                "immunized": immunized
            })

    sim_df = pd.DataFrame(simulated)
    sim_df.to_csv(SIM_FILE, index=False)
    return sim_df

# ---- Simulated Data UI ----
if st.button("📅 Simulate Data (30–60 Days)"):
    sim_df = generate_simulated_data(days=np.random.randint(30, 61), records_per_day=20)
    # Save simulated data as actual patient records
    sim_df[['name', 'age', 'gender', 'symptoms', 'disease']].to_csv(PATIENT_FILE, index=False)
    st.success("Simulated data saved to patient records.")

    st.success("Synthetic health data generated successfully!")
    st.dataframe(sim_df.head(50))

    csv = sim_df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", csv, "simulated_data.csv", "text/csv")
