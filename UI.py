import streamlit as st
import requests
import pandas as pd
import joblib
from gtts import gTTS
import tempfile
from datetime import datetime

# ========================
# 🌿 CONFIGURATION
# ========================
st.set_page_config(
    page_title="Breathify: AI-Powered Air Quality & Health Advisory for Pakistan",
    page_icon="🌿",
    layout="centered",
)

# ========================
# 🌿 STYLING (Modern Header)
# ========================
st.markdown("""
    <style>
        body {
            background-color: #f9fef9;
            color: #222;
            font-family: 'Segoe UI', sans-serif;
        }
        .header {
            text-align: center;
            padding: 40px 20px 30px 20px;
            border-radius: 16px;
            background: linear-gradient(135deg, #a8e6cf, #dcedc1);
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .header h1 {
            color: #2e8b57;
            font-size: 46px;
            font-weight: 800;
            margin-bottom: 10px;
        }
        .header h3 {
            color: #444;
            font-size: 20px;
            margin-bottom: 10px;
        }
        .header p {
            color: #555;
            font-size: 15px;
        }
        .advisory-box {
            padding: 20px;
            border-radius: 12px;
            border-left: 6px solid #2eb872;
            margin-top: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# ========================
# 🌿 APP HEADER
# ========================
st.markdown("""
    <div class="header">
        <h1>🌍 Breathify</h1>
        <h3>AI-Powered Air Quality & Health Advisory for Pakistan</h3>
        <p>Get real-time AQI insights, health tips, and multilingual audio alerts.</p>
    </div>
""", unsafe_allow_html=True)

# ========================
# ⚙️ Load Model
# ========================
MODEL_PATH = r"C:\Users\User\Desktop\AQI project\aqi_lightgbm_model.pkl"

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    st.error(f"❌ Error loading model: {e}")
    st.stop()

# ========================
# 🌦️ API Functions
# ========================
OPENWEATHER_KEY = "YOUR_API_KEY_HERE"  # Replace with your API key

def get_live_data(city_name):
    """Fetch air pollutant and weather data for a given city."""
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},PK&limit=1&appid={OPENWEATHER_KEY}"
    geo_data = requests.get(geo_url).json()
    if not geo_data:
        raise ValueError("City not found or invalid API response.")

    lat, lon = geo_data[0]['lat'], geo_data[0]['lon']
    air_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_KEY}"
    air_data = requests.get(air_url).json()
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,dew_point_2m,precipitation,surface_pressure,wind_speed_10m,wind_direction_10m,shortwave_radiation"
    weather_data = requests.get(weather_url).json()

    if 'current' not in weather_data or 'list' not in air_data:
        raise ValueError("Incomplete data received from APIs.")

    air = air_data['list'][0]['components']
    weather = weather_data['current']

    return pd.DataFrame([{
        "components_co": air.get("co", 0),
        "components_no": air.get("no", 0),
        "components_no2": air.get("no2", 0),
        "components_o3": air.get("o3", 0),
        "components_so2": air.get("so2", 0),
        "components_pm2_5": air.get("pm2_5", 0),
        "components_pm10": air.get("pm10", 0),
        "components_nh3": air.get("nh3", 0),
        "temperature_2m": weather.get("temperature_2m", 0),
        "relative_humidity_2m": weather.get("relative_humidity_2m", 0),
        "dew_point_2m": weather.get("dew_point_2m", 0),
        "precipitation": weather.get("precipitation", 0),
        "surface_pressure": weather.get("surface_pressure", 0),
        "wind_speed_10m": weather.get("wind_speed_10m", 0),
        "wind_direction_10m": weather.get("wind_direction_10m", 0),
        "shortwave_radiation": weather.get("shortwave_radiation", 0)
    }])

# ========================
# 💬 Advisory Function
# ========================
def get_advisory_text(aqi_class, city_name, temperature=None, humidity=None):
    if aqi_class == 1:
        category = "Good"; color = "#a8e6cf"
        en = "✅ Air quality is clean and safe for everyone."
        ur = "ہوا صاف اور محفوظ ہے۔ باہر کھل کر گھومیں۔"
    elif aqi_class == 2:
        category = "Fair"; color = "#dcedc1"
        en = "🙂 Acceptable air quality, but sensitive groups should limit outdoor activity."
        ur = "ہوا معتدل ہے۔ حساس افراد جیسے بچے، بوڑھے اور دمے کے مریض احتیاط کریں۔"
    elif aqi_class == 3:
        category = "Moderate"; color = "#ffd3b6"
        en = "⚠️ Moderate pollution — some people may feel mild discomfort. Wear a mask outdoors."
        ur = "ہوا میں آلودگی معتدل ہے۔ دمے یا دل کے مریض ماسک پہنیں۔"
    elif aqi_class == 4:
        category = "Poor"; color = "#ffaaa5"
        en = "🚫 Unhealthy air. Avoid prolonged outdoor exposure. Use mask and keep kids indoors."
        ur = "ہوا آلودہ ہے۔ بچوں اور بوڑھوں کو گھر پر رکھیں اور ماسک لازمی پہنیں۔"
    else:
        category = "Very Poor"; color = "#ff8b94"
        en = "❗ Extremely unhealthy air. Avoid outdoor exposure completely."
        ur = "انتہائی آلودہ ہوا ہے۔ باہر جانے سے مکمل طور پر گریز کریں۔"

    if humidity and humidity > 70:
        en += " 💧 High humidity can worsen breathing — ensure ventilation."
        ur += " زیادہ نمی سانس لینے میں دشواری پیدا کر سکتی ہے۔"
    if temperature and temperature > 35:
        en += " 🌡️ High temperature — stay hydrated."
        ur += " زیادہ درجہ حرارت میں پانی زیادہ پیئیں۔"

    return category, color, en, ur


# ========================
# 🚀 MAIN APP
# ========================
city_name = st.text_input("🏙️ Enter your city name (e.g., Karachi, Lahore):")

if st.button("🔍 Check Air Quality", key="check"):
    if not city_name:
        st.warning("Please enter a city name.")
    else:
        try:
            df = get_live_data(city_name)
            st.session_state['df'] = df
            st.session_state['city'] = city_name

            prediction = model.predict(df)[0]
            temperature = df["temperature_2m"].values[0]
            humidity = df["relative_humidity_2m"].values[0]

            category, color, en, ur = get_advisory_text(prediction, city_name, temperature, humidity)
            st.session_state.update({
                'prediction': prediction,
                'category': category,
                'color': color,
                'en': en,
                'ur': ur,
                'temperature': temperature,
                'humidity': humidity
            })

        except Exception as e:
            st.error(f"❌ Error fetching data: {e}")

# Show advisory if data exists
if 'prediction' in st.session_state:
    color = st.session_state['color']
    en = st.session_state['en']
    ur = st.session_state['ur']
    category = st.session_state['category']
    city_name = st.session_state['city']

    st.markdown(f"""
    <div class="advisory-box" style="background-color:{color};">
        <h3>🍃 AQI Category: {category}</h3>
        <p>{en}</p>
        <p>🇵🇰 <b>اردو:</b> {ur}</p>
        <p>🏙️ <b>City:</b> {city_name}<br>🕒 {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔊 Play English Voice", key="eng_voice"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_path:
                gTTS(en, lang='en').save(temp_path.name)
                st.audio(temp_path.name)
    with col2:
        if st.button("🔊 Play Urdu Voice", key="urdu_voice"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_path:
                gTTS(ur, lang='ur').save(temp_path.name)
                st.audio(temp_path.name)

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("🍃 Breathify | Developed by Muhammad Sami")