import streamlit as st
import requests
from datetime import date

API_URL = "http://127.0.0.1:8000"

st.title("Gold Loan Manager")

menu = ["Add Customer", "View Customers"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Customer":
    st.header("Add New Customer")
    name = st.text_input("Customer Name")
    gold_weight = st.number_input("Gold Weight (grams)", min_value=0.0)
    loan_amount = st.number_input("Loan Amount", min_value=0.0)
    loan_date = st.date_input("Loan Date", value=date.today())
    photo = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])

    if st.button("Add Customer"):
        data = {
            "name": name,
            "gold_weight": gold_weight,
            "loan_amount": loan_amount,
            "loan_date": str(loan_date)
        }
        resp = requests.post(f"{API_URL}/customers/", json=data)
        if resp.status_code == 200:
            customer = resp.json()
            st.success("Customer added!")
            if photo:
                files = {"file": (photo.name, photo, photo.type)}
                photo_resp = requests.post(f"{API_URL}/customers/{customer['id']}/photo", files=files)
                if photo_resp.status_code == 200:
                    st.success("Photo uploaded!")
                else:
                    st.warning("Photo upload failed.")
        else:
            st.error("Failed to add customer.")

elif choice == "View Customers":
    st.header("All Customers")
    resp = requests.get(f"{API_URL}/customers/")
    if resp.status_code == 200:
        customers = resp.json()
        for c in customers:
            st.subheader(f"{c['name']} (ID: {c['id']})")
            st.write(f"Gold: {c['gold_weight']}g | Loan: ₹{c['loan_amount']} | Date: {c['loan_date']}")
            interest_resp = requests.get(f"{API_URL}/customers/{c['id']}/interest")
            if interest_resp.status_code == 200:
                interest_data = interest_resp.json()
                st.write(f"Interest: ₹{interest_data['interest']:.2f} | Months: {interest_data['months']} | Status: {interest_data['color']}")
            if c['photo_path']:
                st.image(c['photo_path'], width=100)
            st.markdown("---")
    else:
        st.error("Could not fetch customers.")