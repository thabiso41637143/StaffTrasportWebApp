import streamlit as st
import requests
import json
import sqlite3
import pandas as pd

staff_db = sqlite3.connect("staffDatabase.db")
staff_cursor = staff_db.cursor()

def createTable():
    try:
        api_conne = requests.get("https://script.google.com/macros/s/AKfycbyZeOUxL5wj-shkOiysBLaLstwqNf2xRbz5r7MJNHBvdkR2qb2M_GEhxOg09hn-FIeRXg/exec?option=dataReader&menue=passdb")
        staff_tables = json.loads(api_conne.text)
        
        if staff_tables.get('create tables'):
            for query in staff_tables.get('create tables'):
                staff_cursor.execute(query)
            staff_db.commit()
            st.success('Successfully loaded the tables')
        else:
            st.warning("Failed to load tables")
    except ConnectionError:
        st.error(" Failed to connect to the server", icon="🚨")
    except Exception:
        st.error(" An error ocured while trying to connect to the server", icon="🚨")

def userTrips(trips):
    if trips.get('DeleteTrips'):
        staff_cursor.execute(trips.get('DeleteTrips'))
    
    if trips.get('AddTrips'):
        trips.get('AddTrips').pop()
        for query in trips.get('AddTrips'):
            staff_cursor.execute(query)
        staff_db.commit()



data_link = "https://script.google.com/macros/s/AKfycbyZeOUxL5wj-shkOiysBLaLstwqNf2xRbz5r7MJNHBvdkR2qb2M_GEhxOg09hn-FIeRXg/exec?option=dataReader&menue=getUnpaidPassTrip&passId="

createTable()
# Title
st.title("View Trips")

# Input box
user_input = st.text_input("User ID")

# Button
if st.button("View Trips"):
    try:
        st.success(f"Hello, {user_input}!")
        data = requests.get(data_link + user_input)
        userTrips(json.loads(data.text))
        staff_cursor.execute('select tripId, tripDate, fromLoc, toLoc, tripAmount  from Trips WHERE UPPER(passid) = ?', (user_input,))
        df = pd.DataFrame(staff_cursor.fetchall(), columns=["Trip ID", "Trip Date", "From Location", "To Location", "Trip Amount"])
        df["Trip Amount"] = df["Trip Amount"].apply(lambda x: f"R {x:.2f}")
        st.write("List of unpaid trips")
        st.table(df)
    except ConnectionError:
        st.error(' Failed to load your due to connection problem', icon="🚨")
    except Exception:
        st.error(' Something went wrong while loading your trips', icon="🚨")
    

# """
# ["Trip ID", "Trip Date", "From Location", "To Location", "Trip Amount"]

# (tripId, passid, tripAmount, tripDate, fromLoc, toLoc, tripstatus, driverid)
# """