import streamlit as st
import pandas as pd

# Load the seat allotment results and institution data
alloc_df = pd.read_csv("seat_allotment_results.csv", dtype={"CollegeID": "Int64", "PrefNumber": "Int64"})
institutions_df = pd.read_csv("institution_data.csv")

# Merge institution name for better display
alloc_df = alloc_df.merge(institutions_df[['CollegeID', 'Institution']], on='CollegeID', how='left')

# --- Custom CSS for styling ---
st.markdown("""
    <style>
        .main {
            background-color: #f0f4f8;
            padding: 20px;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            font-family: 'Trebuchet MS', sans-serif;
        }
        .stTextInput > div > div > input {
            border: 2px solid #3498db;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        }
        .result-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
            margin-top: 20px;
        }
        .allocated {
            border-left: 6px solid #27ae60;
        }
        .not-allocated {
            border-left: 6px solid #c0392b;
        }
        .info-label {
            color: #34495e;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 Seat Allotment Portal")

# User input
unique_id_input = st.text_input("🔑 Enter Your UniqueID Here")

if unique_id_input:
    # Filter data
    user_alloc = alloc_df[alloc_df['UniqueID'].astype(str) == unique_id_input]

    if user_alloc.empty:
        st.warning("⚠️ No record found for the entered UniqueID.")
    else:
        user_alloc = user_alloc.iloc[0]  # UniqueID unique case
        if user_alloc['CollegeID'] == 0:
            st.info("🚫 No seat allocated based on your rank and preferences.")
        else:
            st.markdown(f"""
                <div class="result-card allocated">
                    <h3>✅ Seat Allocated</h3>
                    <p><span class="info-label">Institution:</span> {user_alloc['Institution']}</p>
                    <p><span class="info-label">College ID:</span> {user_alloc['CollegeID']}</p>
                    <p><span class="info-label">Preference Number Used:</span> {user_alloc['PrefNumber']}</p>
                    <p><span class="info-label">Gender:</span> {user_alloc['Gender']}</p>
                    <p><span class="info-label">Caste:</span> {user_alloc['Caste']}</p>
                </div>
            """, unsafe_allow_html=True)

