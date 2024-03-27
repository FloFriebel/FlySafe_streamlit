import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd

city_couples = {
    "--": "--",
    "Zurich": "Lugano",
    "Lugano": "Zurich",
    "Innsbruck": "Bolzano",
    "Bolzano": "Innsbruck"
}


#st.cache_data
def get_city_data(end_date):
    start_date = end_date - timedelta(days= 20)
    url = f"https://jawp-7s7ugr6oya-ew.a.run.app/predict"
    params = {'_start' : start_date.strftime("%Y-%m-%d"),
              '_end': end_date.strftime("%Y-%m-%d")}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        #st.write(data)
        return data
    else:
        st.error("Failed to retrieve data for the city :sob: ")
        return None

# Function to calculate the difference between two cities' values
def calculate_difference(value1, value2):
    return (value1[0] - value2[0], value1[1] - value2[1], value1[2] - value2[2])

# Function to determine the risk level based on the difference
def determine_risk_level(difference):
    if abs(sum(difference) / 3) < 4:
        st.success("It looks safe up there! :parachute: ")
    elif abs(sum(difference) / 3) > 4 and abs(sum(difference) / 3) < 15:
        st.warning("Be careful, Föhn risk! :tornado: ")
    elif abs(sum(difference) / 3) > 15:
        st.error("Don't fly! :skull_and_crossbones: ")

# Streamlit app
def main():
    st.title("Föhn Warning :parachute: ")
    st.markdown("""
    #### Live forecast for paragliding pilots

    This tool provides a real-time forecast for the next 3 hours. All values are expressed in hectopascals (hPa).
    The threshold for safe flight is set to ±4 hPa, aligning with the criteria for the Föhn phenomenon.
    """)

    selected_city = st.selectbox("Select a city:", list(city_couples.keys()))
    if selected_city != '--':
        # Get the couple city
        couple_city = city_couples[selected_city]

        st.write(f"You selected **{selected_city}** and its twin :two_men_holding_hands: city **{couple_city}**")
        selected_date = datetime.today()

        st.write("Retrieving data...")

        # Fetch data for both cities
        allcity_data = get_city_data(selected_date)
        city1_data = allcity_data[selected_city]
        city2_data = allcity_data[couple_city]


        if city1_data is not None and city2_data is not None:
            # Convert each float to string with two decimal places

            city1_data_rounded = [round(num, 2) for num in city1_data]
            city2_data_rounded = [round(num, 2) for num in city2_data]

            difference = calculate_difference(city1_data, city2_data)

            difference_rounded = [round(num, 2) for num in difference]
            # showing the warning first
            determine_risk_level(difference)
        else:
            st.write("Failed to fetch data from the API. Please try again later.")

        # Creating dataframe for the table
        df = pd.DataFrame([city1_data_rounded, city2_data_rounded, difference_rounded], index = [selected_city, couple_city, 'Difference'], columns = ['+1 hour', '+2 hours', '+3 hours']).T
        st.write('*"Ensuring thorough meteorological checks is essential for achieving safe and joyful landings."* :face_with_monocle: Dr. Zephyr Skywatcher')
        st.write(df)


main()
