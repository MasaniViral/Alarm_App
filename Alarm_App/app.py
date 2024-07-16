import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase app if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_credentials.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://alarmappesp8266-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# Function to fetch alarms from Firebase Realtime Database
def fetch_alarms():
    ref = db.reference('My_Alarm_App/Alarms')
    alarms = ref.get()
    return alarms

# Function to set a new alarm
def set_alarm(alarm_time):
    ref = db.reference('My_Alarm_App/Alarms')
    alarms = ref.get()
    if not alarms:
        alarms = {}
    alarm_id = f'Alarm_{len(alarms) + 1}'
    ref.child(alarm_id).set(alarm_time)

# Function to delete an alarm
def delete_alarm(alarm_id):
    ref = db.reference(f'My_Alarm_App/Alarms/{alarm_id}')
    ref.delete()

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
        font-family: Arial, sans-serif;
    }
    .container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .header {
        text-align: center;
        padding-bottom: 20px;
        border-bottom: 1px solid #ddd;
    }
    .header h1 {
        margin: 0;
        color: #333333;
    }
    .form-container {
        margin-top: 30px;
    }
    .form-container input {
        width: calc(100% - 24px);
        padding: 12px;
        margin-bottom: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    .form-container button {
        width: 100%;
        padding: 12px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
    }
    .form-container button:hover {
        background-color: #0056b3;
    }
    .alarms-container {
        margin-top: 40px;
    }
    .alarm-item {
        padding: 15px;
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 5px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .alarm-item span {
        font-size: 16px;
        color: #333;
    }
    .delete-button {
        background-color: #dc3545;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px;
        cursor: pointer;
        font-size: 16px;
    }
    .delete-button:hover {
        background-color: #c82333;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI
st.markdown("<div class='container'>", unsafe_allow_html=True)
st.markdown("<div class='header'><h1>Alarm App</h1></div>", unsafe_allow_html=True)

st.markdown("<div class='form-container'>", unsafe_allow_html=True)
st.markdown("<h2>Set a New Alarm</h2>", unsafe_allow_html=True)
alarm_time = st.text_input("", placeholder="Enter alarm time (HH:MM)")
if st.button("Set Alarm"):
    set_alarm(alarm_time)
    st.success(f"Alarm set for {alarm_time}")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='alarms-container'>", unsafe_allow_html=True)
st.markdown("<h2>Current Alarms</h2>", unsafe_allow_html=True)
alarms = fetch_alarms()
if alarms:
    for alarm_id, alarm_time in alarms.items():
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"<span>{alarm_id}</span>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<span>{alarm_time}</span>", unsafe_allow_html=True)
        with col3:
            if st.button("Delete", key=alarm_id):
                delete_alarm(alarm_id)
                st.experimental_rerun()
else:
    st.write("No alarms set.")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
