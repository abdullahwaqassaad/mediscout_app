import streamlit as st  
import pandas as pd  
import os  
import matplotlib.pyplot as plt  

# Files for storing users and patients  
USERS_FILE = 'users.csv'  
PATIENTS_FILE = 'patients.csv'  

# Function to load or create user data  
def load_users():  
    if os.path.exists(USERS_FILE):  
        return pd.read_csv(USERS_FILE)  
    else:  
        df_users = pd.DataFrame({'username': ['admin'], 'password': ['admin']})  
        df_users.to_csv(USERS_FILE, index=False)  
        return df_users  

# Function to load or create patient data  
def load_patients():  
    if os.path.exists(PATIENTS_FILE):  
        return pd.read_csv(PATIENTS_FILE)  
    else:  
        data = {  
            'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  
            'symptoms': [  
                'Fever', 'Cough', 'Headache', 'Sore Throat', 'Nausea',  
                'Fatigue', 'Shortness of Breath', 'Muscle Pain', 'Dizziness', 'Runny Nose'  
            ],  
            'diseases': [  
                'Malaria', 'Flu', 'Migraine', 'Phraryngitis', 'Gastroenteritis',  
                'Anemia', 'Asthma', 'Influenza', 'Vertigo', 'Common Cold'  
            ],  
            'lat': [25.0, 24.8, 25.2, 24.9, 25.1, 24.7, 25.3, 24.9, 25.0, 24.8],  
            'lon': [67.0, 67.2, 67.1, 67.3, 67.4, 67.2, 67.1, 67.3, 67.2, 67.4],  
            'disease_flag': [1, 1, 1, 1, 1, 0, 0, 1, 0, 0],  
            'age': [25, 30, 45, 22, 60, 35, 40, 50, 29, 33],  
            'gender': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female']  
        }  
        df_patients = pd.DataFrame(data)  
        df_patients.to_csv(PATIENTS_FILE, index=False)  
        return df_patients  

# --- Authentication Pages ---  
def login_page():  
    st.title("Login")  
    username = st.text_input("Username")  
    password = st.text_input("Password", type='password')  
    users_df = load_users()  
    if st.button("Login"):  
        if username in users_df['username'].values:  
            if (users_df[users_df['username'] == username]['password'].values[0]) == password:  
                st.session_state['logged_in'] = True  
                st.session_state['username'] = username  
                st.success(f"Welcome {username}!")  
            else:  
                st.error("Incorrect password.")  
        else:  
            st.error("User not found. Please Sign Up.")  

def signup_page():  
    st.title("Sign Up")  
    new_username = st.text_input("Choose a Username")  
    new_password = st.text_input("Choose Password", type='password')  
    if st.button("Sign Up"):  
        users_df = load_users()  
        if new_username in users_df['username'].values:  
            st.error("Username already exists!")  
        else:  
            new_user = pd.DataFrame({'username':[new_username],'password':[new_password]})  
            users_df = pd.concat([users_df, new_user], ignore_index=True)  
            users_df.to_csv(USERS_FILE, index=False)  
            st.success("Account created! Please go to Login.")  

# --- Main Dashboard ---  
def main_app():  
    st.title("MediScout Pakistan Dashboard")  
    df_patients = load_patients()  

    # Sidebar options  
    option = st.sidebar.radio("Navigation", ["Dashboard", "Patient Management", "Search Patient"])  

    if option == "Dashboard":
    st.header("Disease Data Visualization and Filter")
    df_patients = load_patients()

    # Filters
    selected_symptom = st.selectbox("Select Symptom", df_patients['symptoms'].unique())

    # Age range slider from 1 to 120
    age_min, age_max = 1, 120
    age_range = st.slider("Select Age Range", min_value=age_min, max_value=age_max, value=(age_min, age_max))

    # Gender filter with 'All' option
    selected_gender = st.selectbox("Select Gender", ['All'] + list(df_patients['gender'].unique()))

    # Apply filters
    filtered_df = df_patients[df_patients['symptoms'] == selected_symptom]
    filtered_df = filtered_df[
        (filtered_df['age'] >= age_range[0]) & (filtered_df['age'] <= age_range[1])
    ]
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['gender'] == selected_gender]

    # Show filtered data
    st.write("Filtered Data:", filtered_df)

    # Map visualization
    if not filtered_df.empty:
        st.map(filtered_df[['lat', 'lon']])
    else:
        st.write("No data to display on map for selected filters.")

    # Plot disease counts
    st.header("Disease Counts")
    if not filtered_df.empty:
        fig, ax = plt.subplots()
        filtered_df['diseases'].value_counts().plot.bar(ax=ax)
        ax.set_xlabel("Disease")
        ax.set_ylabel("Count")
        st.pyplot(fig)
    else:
        st.write("No data to display for the selected filters.")

# Continue with plotting Disease Counts if data exists
if not filtered_df.empty:
    # Plot disease counts
    st.header("Disease Counts")
    fig, ax = plt.subplots()
    filtered_df['diseases'].value_counts().plot.bar(ax=ax)
    ax.set_xlabel("Disease")
    ax.set_ylabel("Count")
    st.pyplot(fig)
else:
    # No data case
    st.write("No data to display for the selected filters.")
    # Inside the 'Dashboard' section after map display:
if not filtered_df.empty:
    st.map(filtered_df[['lat', 'lon']])
else:
    st.write("No data to display for the selected filters.")

# Now, from the line you pointed out:
st.write("No data to display for the selected filters.")

# Continue with plotting disease counts if data exists
if not filtered_df.empty:
    st.header("Disease Counts")
    fig, ax = plt.subplots()
    filtered_df['diseases'].value_counts().plot.bar(ax=ax)
    ax.set_xlabel("Disease")
    ax.set_ylabel("Count")
    st.pyplot(fig)
else:
    # No data case
    st.write("No data to display for the selected filters.")
# Continue with any additional visualizations or summaries if desired
# For example, display the filtered data
st.dataframe(filtered_df)
