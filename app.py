import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="MediScout Pakistan", layout="wide")

# --- USER MANAGEMENT ---
USERS_FILE = 'users.csv'
PATIENT_FILE = 'patients.csv'

def load_users():
    if os.path.exists(USERS_FILE):
        return pd.read_csv(USERS_FILE)
    else:
        return pd.DataFrame(columns=['username', 'password'])

def save_user(username, password):
    users_df = load_users()
    if username in users_df['username'].values:
        return False
    users_df = users_df.append({'username': username, 'password': password}, ignore_index=True)
    users_df.to_csv(USERS_FILE, index=False)
    return True

def authenticate(username, password):
    users_df = load_users()
    return not users_df[(users_df['username'] == username) & (users_df['password'] == password)].empty

# --- SESSION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# --- LOGIN / SIGNUP ---
if not st.session_state.logged_in:
    choice = st.sidebar.selectbox("Login or Signup", ['Login', 'Signup'])

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if choice == 'Login':
        if st.sidebar.button("Login"):
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
            else:
                st.error("Invalid credentials.")
    else:
        if st.sidebar.button("Signup"):
            if save_user(username, password):
                st.success("User registered. Please login.")
            else:
                st.error("Username already exists.")
    st.stop()

# --- WELCOME ---
st.sidebar.success(f"Welcome, {st.session_state.username}!")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.experimental_rerun()

# --- EXISTING DATA ---
data = {
    'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'symptoms': ['Fever', 'Cough', 'Headache', 'Sore Throat', 'Nausea', 'Fatigue', 'Shortness of Breath', 'Muscle Pain', 'Dizziness', 'Runny Nose'],
    'diseases': ['Malaria', 'Flu', 'Migraine', 'Phraryngitis', 'Gastroenteritis', 'Anemia', 'Asthma', 'Influenza', 'Vertigo', 'Common Cold'],
    'lat': [25.0, 24.8, 25.2, 24.9, 25.1, 24.7, 25.3, 24.9, 25.0, 24.8],
    'lon': [67.0, 67.2, 67.1, 67.3, 67.4, 67.2, 67.1, 67.3, 67.2, 67.4],
    'disease_flag': [1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
    'age': [25, 30, 45, 22, 60, 35, 40, 50, 29, 33],
    'gender': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female']
}
df = pd.DataFrame(data)

# --- MAIN APP ---
st.title("🧠 MediScout Pakistan Prototype")

# Show/Hide Form
if 'show_form' not in st.session_state:
    st.session_state.show_form = False

if st.button("Register New Patient"):
    st.session_state.show_form = not st.session_state.show_form

if st.session_state.show_form:
    st.subheader("Patient Registration Form")
    with st.form("patient_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120)
        gender = st.selectbox("Gender", ['Male', 'Female', 'Other'])
        symptoms_input = st.text_input("Symptoms (comma separated)")
        disease_input = st.text_input("Disease")
        submitted = st.form_submit_button("Add Patient Data")
        if submitted:
            if os.path.exists(PATIENT_FILE):
                patients_df = pd.read_csv(PATIENT_FILE)
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
            patients_df.to_csv(PATIENT_FILE, index=False)
            st.success(f"Patient {name} data added!")

# --- DELETE PATIENT ---
st.subheader("🗑️ Delete Patient Record")
del_name = st.text_input("Enter Patient Name to Delete")
if st.button("Delete Patient"):
    if os.path.exists(PATIENT_FILE):
        patients_df = pd.read_csv(PATIENT_FILE)
        if del_name in patients_df['name'].values:
            patients_df = patients_df[patients_df['name'] != del_name]
            patients_df.to_csv(PATIENT_FILE, index=False)
            st.success(f"Deleted patient record: {del_name}")
        else:
            st.error("Patient not found.")
    else:
        st.warning("No patient data found.")

# --- SEARCH PATIENT ---
st.subheader("🔍 Search Patient")
search_name = st.text_input("Search by Patient Name")
if st.button("Search"):
    if os.path.exists(PATIENT_FILE):
        patients_df = pd.read_csv(PATIENT_FILE)
        record = patients_df[patients_df['name'].str.lower() == search_name.lower()]
        if not record.empty:
            st.success("Patient Record Found:")
            st.dataframe(record)
        else:
            st.warning("No record found.")
    else:
        st.warning("Patient database not found.")

# --- FILTERS AND VISUALIZATION ---
st.header("📊 Filter Disease Data")
selected_symptom = st.selectbox("Select Symptom", df['symptoms'].unique())
age_range = st.slider("Select Age Range", min_value=1, max_value=120, value=(1, 120))
selected_gender = st.selectbox("Select Gender", ['Select'] + list(df['gender'].unique()))

# Apply filters
filtered_df = df[df['symptoms'] == selected_symptom]
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
    st.info("No data to display for the selected filters.")
