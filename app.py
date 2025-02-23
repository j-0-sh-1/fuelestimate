import streamlit as st
import pandas as pd
from datetime import datetime
from pymongo import MongoClient

# MongoDB Connection
MONGO_URI = ("mongodb+srv://joshuailangovansamuel:HHXm1xKAsKxZtQ6I@"
             "cluster0.pbvcd.mongodb.net/fuel_records?retryWrites=true&w=majority&appName=Cluster0")
client = MongoClient(MONGO_URI)
try:
    client.admin.command('ping')
    st.sidebar.success("MongoDB Connected!")
except Exception as e:
    st.sidebar.error("MongoDB connection error: " + str(e))

# Database and collection
db = client["fuel_records"]
submissions_collection = db["submissions"]

# Title of the app
st.title("Fuel Tracker App")

# Input fields
st.header("Enter Your Car Details")
current_km = st.number_input("Current Kilometer Reading", min_value=0.0, step=1.0)
mileage = st.number_input("Mileage (km per liter)", min_value=1.0, step=0.1, value=16.0)
fuel_filled = st.number_input("Fuel Filled (liters)", min_value=0.0, step=0.1)
reading_date = st.date_input("Date of Reading", value=datetime.now())
fuel_date = st.date_input("Date of Fuel Fill", value=datetime.now())

# Check if dates match
if reading_date != fuel_date:
    st.error("Error: Date of reading and fuel fill must be the same!")
else:
    # Calculate range and refuel point
    if st.button("Calculate"):
        # Total distance possible with filled fuel
        total_range = fuel_filled * mileage
        km_till_refuel = current_km + total_range

        # Display results
        st.success(f"You can drive up to **{km_till_refuel:.2f} km** with {fuel_filled} liters.")
        st.info(f"Refuel when your odometer reaches approximately **{km_till_refuel:.2f} km**.")

        # Save data to MongoDB
        submission = {
            "date": reading_date.strftime("%Y-%m-%d"),
            "current_km": current_km,
            "mileage_km_per_l": mileage,
            "fuel_filled_l": fuel_filled,
            "max_km": km_till_refuel,
            "timestamp": datetime.now().isoformat()  # For sorting purposes
        }
        submissions_collection.insert_one(submission)
        st.write("Data saved to MongoDB successfully!")

# Show past records
st.header("Past Fuel Records")
records = submissions_collection.find().sort("timestamp", -1)  # Sort by latest first
records_list = list(records)  # Convert cursor to list

if records_list:
    # Convert to DataFrame for display
    df = pd.DataFrame(records_list)
    df = df.drop(columns=["_id", "timestamp"])  # Hide MongoDB ID and timestamp
    st.dataframe(df)
else:
    st.write("No records yet. Calculate something to start!")
