import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd
#import folium
#from streamlit_folium import folium_static

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
    The threshold interval for safe flight is set to ±4 hPa, aligning with the criteria for the Föhn phenomenon.
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
            city1_data_rounded_hPa = [f'{pressure} hPa' for pressure in city1_data_rounded]
            city2_data_rounded_hPa = [f'{pressure} hPa' for pressure in city2_data_rounded]
            difference = calculate_difference(city1_data, city2_data)

            difference_rounded = [round(num, 2) for num in difference]
            difference_rounded_hPa = [f'{difference} hPa' for difference in difference_rounded]
            # showing the warning first
            determine_risk_level(difference)
        else:
            st.write("Failed to fetch data from the API. Please try again later.")

        # Creating dataframe for the table
        #df = pd.DataFrame([city1_data_rounded, city2_data_rounded, difference_rounded], index = [selected_city, couple_city, 'Difference'], columns = ['+1 hour', '+2 hours', '+3 hours']).T
        # Get current hour
        current_hour = datetime.now().strftime('%H')
        current_hour = int(current_hour)
        column_names = [f'{(current_hour + i) % 24}:00' for i in range(1, 4)]

        df = pd.DataFrame([city1_data_rounded_hPa, city2_data_rounded_hPa, difference_rounded_hPa],
                          index=[selected_city, couple_city, 'Pressure Difference'], columns=column_names).T



        st.write('*"Ensuring thorough meteorological checks is essential for achieving safe and joyful landings."* :face_with_monocle: Dr. Zephyr Skywatcher')
        st.write(df)

        # st.title("City Map")
        #     # Create a Folium map centered around a specific location
        # # Create a Folium map centered around a specific location
        # m = folium.Map(location=[47.05, 9.5], zoom_start=7)

        # # Add markers for each city
        # city_coordinates = {
        #     "Zurich": (47.3769, 8.5417),
        #     "Lugano": (46.0052, 8.9535),
        #     "Innsbruck": (47.2692, 11.4041),
        #     "Bolzano": (46.4983, 11.3548)
        # }
        # for city, coordinates in city_coordinates.items():
        #     folium.Marker(location=coordinates, popup=city).add_to(m)

        # # Display the map using Streamlit
        # folium_static(m)



main()
