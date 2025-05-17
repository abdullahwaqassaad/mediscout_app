import streamlit as st
import pandas as pd
import os
import random
import datetime
from faker import Faker
import matplotlib.pyplot as plt

# ---- CONFIG ----
st.set_page_config(page_title="MediScout Pakistan", layout="wide")
USERS_FILE = 'users.csv'
PATIENT_FILE = 'patients.csv'
SIMULATION_FILE = 'simulation.csv'

fake = Faker()

# ---- SESSION STATE ----
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'show_form' not in st.session_state:
    st.session_state.show_form = False
if 'show_simulation' not in st.session_state:
    st.session_state.show_simulation = False

# ---- USER MANAGEMENT FUNCTIONS ----
def load_users():
    if os.path.exists(USERS_FILE):
        try:
            return pd.read_csv(USERS_FILE)
        except:
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
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.experimental_rerun()
            else:
                st.sidebar.error("Invalid username or password.")
    else:
        if st.sidebar.button("Signup"):
            if save_user(username, password):
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

# ---- SYNTHETIC DATA SIMULATION ----
def simulate_health_data(num_records=50):
    diseases = ['Dengue', 'Diarrhea', 'Stunting', 'Wasting', 'Tuberculosis', 'Hypertension', 'Diabetes', 'ARI']
    simulation_data = []
    start_date = datetime.date.today() - datetime.timedelta(days=60)
    for _ in range(num_records):
        age = random.randint(0, 80)
        gender = random.choice(['Male', 'Female'])
        date = start_date + datetime.timedelta(days=random.randint(0, 60))
        fever = random.choices([True, False], weights=[25, 75])[0]  # 25% have fever
        diarrhea = random.choices([True, False], weights=[39, 61])[0] if age < 5 else False
        stunting = random.choices([True, False], weights=[38, 62])[0] if age < 5 else False
        wasting = random.choices([True, False], weights=[17.7, 82.3])[0] if age < 5 else False
        tb = random.choices([True, False], weights=[259, 999741])[0]
        hypertension = random.choices([True, False], weights=[37.3, 62.7])[0] if 18 <= age <= 69 else False
        diabetes = random.choices([True, False], weights=[31.4, 68.6])[0] if 18 <= age else False
        ari = random.choices([True, False], weights=[75, 25])[0] if age < 5 else False
        disease = random.choice(diseases) if fever or diarrhea or tb or hypertension or diabetes or ari else 'Healthy'

        simulation_data.append({
            'date': date,
            'name': fake.name(),
            'age': age,
            'gender': gender,
            'fever': fever,
            'diarrhea': diarrhea,
            'stunting': stunting,
            'wasting': wasting,
            'tb': tb,
            'hypertension': hypertension,
            'diabetes': diabetes,
            'ari': ari,
            'disease': disease
        })

    df = pd.DataFrame(simulation_data)
    df.to_csv(SIMULATION_FILE, index=False)
    return df

def load_simulation():
    if os.path.exists(SIMULATION_FILE):
        return pd.read_csv(SIMULATION_FILE)
    else:
        return pd.DataFrame()

# ---- MAIN UI ----
st.title("🧠 MediScout Pakistan Prototype")

# ---- Simulate Data ----
if st.button("📊 Simulate Health Data"):
    st.session_state.show_simulation = not st.session_state.show_simulation

if st.session_state.show_simulation:
    num_records = st.slider("Number of Records to Simulate", 10, 200, 50)
    if st.button("Generate Data"):
        simulated_data = simulate_health_data(num_records)
        st.success(f"Simulated {num_records} community health observations.")
        st.dataframe(simulated_data)

# ---- Existing Features: Patient Registration ----
if st.button("➕ Register New Patient"):
    st.session_state.show_form = not st.session_state.show_form

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

# ---- Load Simulated Data ----
st.subheader("📊 View Simulated Data")
simulation_df = load_simulation()
if not simulation_df.empty:
    st.dataframe(simulation_df)
else:
    st.warning("No simulated data available. Generate data to view.")
