import streamlit as st
import requests
import pandas as pd
from datetime import date

API_URL="http://127.0.0.1:8000"



st.markdown("""
<style>

    /* Main App Background */
    .stApp {
        background-color: #E0F2F7;  /* Light soothing blue for hospital theme */
    }

    /* Title */
    h1 {
        color: #1E40AF;  /* Deep blue for a professional look */
        font-weight: 700;
        text-align: center;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #BEE3F8;  /* Soft blue for sidebar */
    }

    /* Sidebar Dropdown */
    section[data-testid="stSidebar"] div[role="combobox"] {
        background-color: white;
        border-radius: 8px;
    }

    /* Tables */
    thead tr th {
        background-color: #1E40AF !important;  /* Matches title */
        color: white !important;
    }

    tbody tr:hover {
        background-color: #BFDBFE !important;  /* Light blue hover for table rows */
    }

    /* Buttons */
    .stButton > button {
        background-color: #0EA5E9;  /* Blue hospital theme */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #0284C7;  /* Darker blue on hover */
        color: white;
    }

    /* Input Boxes */
    .stTextInput input,
    .stNumberInput input,
    .stDateInput input {
        border-radius: 8px;
    }

    /* Subheaders */
    h3 {
        color: #1F2933;
        font-weight: 600;
    }

</style>
""", unsafe_allow_html=True)
#------------------------------------------------------

st.set_page_config(page_title="Hospital Patient Management System", page_icon="🏥")
st.markdown("<h1 style='color:#2E86C1;'>🏥 Hospital Patient Management System</h1>", unsafe_allow_html=True)

#-----------------MENU--------------------
menu = st.sidebar.selectbox(
    "📌 Navigation Menu",
    ["📋 View Patient Details", "➕ Add Patient Details", "✏ Update Patient Details", "🗑 Delete Patient Details"]
)

#---------------VIEW----------------
if menu == "📋 View Patient Details":

    st.subheader("🛏️ Admitted Patients")

    response = requests.get(f"{API_URL}/patients")

    if response.status_code == 200:
        data = response.json()

        if len(data) == 0:
            st.warning("⚠ No patients found")
        else:
            df = pd.DataFrame(data)
            st.dataframe(df.sort_values("id"))

    else:
        st.error("❌ Failed to fetch patient details from API")

#---------------ADD--------------
elif menu == "➕ Add Patient Details":
    st.info("📌 Enter patient details carefully")
    name = st.text_input("👤 Patient Name")
    age = int(st.number_input("🎂 Age",min_value=1,step=1))
    disease = st.text_input("🩺 Disease")
    admission_date=st.date_input("📅 Admission Date (Optional)")

    if st.button("✅ Admit Patient"):

        if name.strip() == "":
            st.warning("⚠ Patient Name cannot be empty")
        elif age<0:
            st.warning("⚠ Age must be greater than 0")
        elif disease.strip()=="":
            st.warning("⚠ Disease cannot be empty")
        else:
            final_date=admission_date if admission_date else date.today()

            payload = {
                "patient_name": name,
                "age": age,
                "disease": disease,
                "admission_date":str(final_date)       
            }

            response = requests.post(f"{API_URL}/patients", json=payload)

            if response.status_code == 200:
                st.success("🎉 Patient Admitted!")
                st.write("If any inconvenience please inform!")

            else:
                st.error("❌ Failed to admit patient")


#--------------UPDATE----------------
elif menu == "✏ Update Patient Details":
    st.info("✏ Update Patient Details ")
    patient_id = st.number_input("🔢 Enter Patient ID", min_value=1,step=1)
    name = st.text_input("👤 Patient Name")
    age = int(st.number_input("🎂 Age",min_value=1,step=1))
    disease = st.text_input("🩺 Disease")
    admission_date = st.date_input("📅 Admission Date")

    if st.button("🚀 Update Patient"):

        if name.strip() == "":
            st.warning("⚠ Patient Name cannot be empty")
        elif age<0:
            st.warning("⚠ Age must be greater than 0")
        elif disease.strip()=="":
            st.warning("⚠ Disease cannot be empty")
        else:
            payload = {
                "patient_name": name,
                "age": age,
                "disease": disease
            }

            if admission_date:
                payload["admission_date"]=str(admission_date)


            response = requests.put(f"{API_URL}/patients/{patient_id}", json=payload)

            if response.status_code == 200:
                st.success("✅ Patient Details Updated Successfully!")
            elif response.status_code==404:
                st.warning("⚠ Patient details not found")
            else:
                st.error("❌ Failed to update patient details")



#--------------------DELETE----------------------
elif menu == "🗑 Delete Patient Details":

    st.error("🗑 Delete Patient Record")

    patient_id = st.number_input("🔢 Enter Patient ID to Delete", min_value=1,step=1)

    if st.button("❌ Delete Patient"):

        response = requests.delete(f"{API_URL}/patients/{patient_id}")

        if response.status_code == 200:
            st.success("🗑 Discharged/Patient Record Deleted Successfully!")
        elif response.status_code==404:
            st.warning("⚠ Patient details not found")
        else:
            st.error("❌ Failed to delete patient details")
