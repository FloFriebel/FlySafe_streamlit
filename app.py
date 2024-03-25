import streamlit as st
import requests
from datetime import datetime

city_couples = {
    "Zurich": "Lugano",
    "Lugano": "Zurich",
    "Innsbruck": "Bolzano",
    "Bolzano": "Innsbruck"
}



def get_city_data(city):
    start_date = "2024-02-10"
    end_date = "2024-03-15"
#f"http://127.0.0.1:8000/predict/{city}?_start={start_date}&_end={end_date}"
    #url = f"https://api.example.com/data/{city}?api_key=API_KEY"
    url = f"http://127.0.0.1:8000/predict"
    #params = {'_start':datetime.today().strftime('%Y-%m-%d'), '_end': datetime.today().strftime('%Y-%m-%d')}

    if st.button('air pressure'):
        params = {'_start' : start_date, '_end': end_date}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            st.write(data)
            return data.get("value")
        else:
            st.error("Failed to retrieve data for the city :sob: ")
            return None

# Function to calculate the difference between two cities' values
def calculate_difference(value1, value2):
    return value1 - value2

# Function to determine the risk level based on the difference
def determine_risk_level(difference):
    if abs(difference) > 4:
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

    #selected_date = st.date_input("Select a date for prediction", datetime.today())

    st.write("Retrieving data...")

    # Fetch data for both cities
    city1_data = get_city_data(selected_city)
    city2_data = get_city_data(couple_city)


    if city1_data is not None and city2_data is not None:
        st.write(f"Forecasted pressure(hPa) for {selected_city}: {city1_data}")
        st.write(f"Forecasted pressure(hPa) for {couple_city}: {city2_data}")

        difference = calculate_difference(city1_data, city2_data)
        st.write(f"hPa difference between {selected_city} and {couple_city}: {difference}")

        risk_level = determine_risk_level(difference)
        st.write(risk_level)
    else:
        st.write("Failed to fetch data from the API. Please try again later.")


main()
