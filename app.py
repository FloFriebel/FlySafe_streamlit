import streamlit as st
import requests
from datetime import datetime, timedelta

city_couples = {
    "Zurich": "Lugano",
    "Lugano": "Zurich",
    "Innsbruck": "Bolzano",
    "Bolzano": "Innsbruck"
}


st.cache_data
def get_city_data(end_date):
    start_date = end_date - timedelta(days= 20)
    url = f"https://jawp-7s7ugr6oya-ew.a.run.app/predict"
    if st.button('air pressure'):
        params = {'_start' : start_date, '_end': end_date}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            st.write(data)
            return data
        else:
            st.error("Failed to retrieve data for the city :sob: ")
            return None

# Function to calculate the difference between two cities' values
def calculate_difference(value1, value2):
    return (value1[0] - value2[0], value1[1] - value2[1], value1[2] - value2[2])

# Function to determine the risk level based on the difference
def determine_risk_level(difference):
    if abs(sum(difference) / 3) > 4:
        return "Be careful, Foehn risk! :dash:"
    else:
        return "It looks safe up there! :+1:"

# Streamlit app
def main():
    st.title("Foehn predictions for paragliders")
    #can add a short description

    selected_city = st.selectbox("Select a city:", list(city_couples.keys()))

    # Get the couple city
    couple_city = city_couples[selected_city]

    st.write(f"You selected {selected_city} and its twin :two_men_holding_hands: {couple_city}")


    selected_date = st.date_input("Select a date for prediction", datetime.today())

    st.write("Retrieving data...")

    # Fetch data for both cities
    allcity_data = get_city_data(selected_date)
    #st.write(allcity_data)


    city1_data = allcity_data[selected_city]
    city2_data = allcity_data[couple_city]


    #st.write(city1_data)


    if city1_data is not None and city2_data is not None:
        # Convert each float to string with two decimal places
        formatted_data_city1 = [f"{pressure:.2f}" for pressure in city1_data]
        formatted_string1 = ", ".join(formatted_data_city1)
        st.write(f"3 hours pressure forecast(hPa) for {selected_city}: {formatted_string1}")
        #st.write(f"Forecasted pressure(hPa) for {selected_city}: {city1_data}")
        formatted_data_city2 = [f"{pressure:.2f}" for pressure in city2_data]
        formatted_string2 = ", ".join(formatted_data_city2)
        st.write(f"3 hours pressure forecast(hPa) for {couple_city}: {formatted_string2}")

        difference = calculate_difference(city1_data, city2_data)
        formatted_difference = [f"{diff:.2f}" for diff in difference]
        formatted_difference_string = ", ".join(formatted_difference)
        st.write(f"Forecasted hPa difference between {selected_city} and {couple_city}: {formatted_difference_string}")

        risk_level = determine_risk_level(difference)
        st.write(risk_level)
    else:
        st.write("Failed to fetch data from the API. Please try again later.")


main()
