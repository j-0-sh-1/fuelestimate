import streamlit as st
import pandas as pd
from datetime import datetime
import os

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

        # Save data to CSV
        data = {
            "Date": [reading_date.strftime("%Y-%m-%d")],
            "Current_KM": [current_km],
            "Mileage_km_per_L": [mileage],
            "Fuel_Filled_L": [fuel_filled],
            "Max_KM": [km_till_refuel]
        }
        df = pd.DataFrame(data)

        # Append to file if it exists, otherwise create new
        file_path = "fuel_records.csv"
        if os.path.exists(file_path):
            existing_df = pd.read_csv(file_path)
            updated_df = pd.concat([existing_df, df], ignore_index=True)
            updated_df.to_csv(file_path, index=False)
        else:
            df.to_csv(file_path, index=False)

        st.write("Data saved successfully!")

# Show past records
st.header("Past Fuel Records")
if os.path.exists("fuel_records.csv"):
    records = pd.read_csv("fuel_records.csv")
    st.dataframe(records)
else:
    st.write("No records yet. Calculate something to start!")