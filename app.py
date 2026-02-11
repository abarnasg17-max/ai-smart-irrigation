import streamlit as st
import requests
import pandas as pd

# ---------------- CONFIG ----------------
API_KEY = "cd7c64ae1d8ad11ce323be2d781069eb"  # 🔑 Paste your OpenWeather API key

st.set_page_config(page_title="AI Smart Irrigation", page_icon="🌱", layout="centered")

# ---------------- LANGUAGE DICTIONARY ----------------
translations = {

    "English": {
        "title": "🌱 AI-Driven Smart Irrigation & Water Optimization System",
        "subtitle": "Real-time AI decision support for rain-fed agriculture",
        "select_city": "📍 Select Your City",
        "select_crop": "🌾 Select Crop Type",
        "weather": "🌦 Live Weather Data",
        "temp": "Temperature",
        "humidity": "Humidity",
        "rain": "Rainfall (last 1 hour)",
        "map": "🗺 Farm Location Map",
        "recommend": "🤖 AI Recommendation",
        "irrigate": "💦 Irrigation Needed",
        "no_irrigate": "✅ No Irrigation Needed",
        "score_today": "Water Optimization Score (Today)",
        "score_yest": "Water Optimization Score (Yesterday)",
        "compare": "📊 Today vs Yesterday Comparison",
        "explain": "🧠 AI Explanation"
    },

    "Tamil": {
        "title": "🌱 AI சாகுபடி நீர்ப்பாசன & நீர் மேம்பாட்டு அமைப்பு",
        "subtitle": "மழை சார்ந்த விவசாயத்திற்கான நேரடி AI முடிவு ஆதரவு",
        "select_city": "📍 உங்கள் நகரத்தை தேர்வு செய்யவும்",
        "select_crop": "🌾 பயிர் வகையை தேர்வு செய்யவும்",
        "weather": "🌦 நேரடி வானிலை தகவல்",
        "temp": "வெப்பநிலை",
        "humidity": "ஈரப்பதம்",
        "rain": "மழை (கடைசி 1 மணி நேரம்)",
        "map": "🗺 பண்ணை இருப்பிட வரைபடம்",
        "recommend": "🤖 AI பரிந்துரை",
        "irrigate": "💦 நீர்ப்பாசனம் தேவை",
        "no_irrigate": "✅ நீர்ப்பாசனம் தேவையில்லை",
        "score_today": "இன்றைய நீர் மேம்பாட்டு மதிப்பெண்",
        "score_yest": "நேற்றைய நீர் மேம்பாட்டு மதிப்பெண்",
        "compare": "📊 இன்று மற்றும் நேற்று ஒப்பீடு",
        "explain": "🧠 AI விளக்கம்"
    },

    "Hindi": {
        "title": "🌱 एआई आधारित स्मार्ट सिंचाई एवं जल अनुकूलन प्रणाली",
        "subtitle": "वर्षा आधारित कृषि के लिए रियल-टाइम एआई निर्णय समर्थन",
        "select_city": "📍 अपना शहर चुनें",
        "select_crop": "🌾 फसल प्रकार चुनें",
        "weather": "🌦 लाइव मौसम डेटा",
        "temp": "तापमान",
        "humidity": "आर्द्रता",
        "rain": "पिछले 1 घंटे की वर्षा",
        "map": "🗺 खेत का स्थान मानचित्र",
        "recommend": "🤖 एआई सिफारिश",
        "irrigate": "💦 सिंचाई आवश्यक",
        "no_irrigate": "✅ सिंचाई आवश्यक नहीं",
        "score_today": "आज का जल अनुकूलन स्कोर",
        "score_yest": "कल का जल अनुकूलन स्कोर",
        "compare": "📊 आज बनाम कल तुलना",
        "explain": "🧠 एआई विश्लेषण"
    },

    "Telugu": {
        "title": "🌱 AI ఆధారిత స్మార్ట్ నీటి పథకం వ్యవస్థ",
        "subtitle": "వర్షాధార వ్యవసాయం కోసం రియల్ టైమ్ AI నిర్ణయ సహాయం",
        "select_city": "📍 మీ నగరాన్ని ఎంచుకోండి",
        "select_crop": "🌾 పంట రకాన్ని ఎంచుకోండి",
        "weather": "🌦 ప్రత్యక్ష వాతావరణ సమాచారం",
        "temp": "ఉష్ణోగ్రత",
        "humidity": "ఆర్ద్రత",
        "rain": "గత 1 గంట వర్షపాతం",
        "map": "🗺 వ్యవసాయ స్థలం మ్యాప్",
        "recommend": "🤖 AI సిఫార్సు",
        "irrigate": "💦 నీటిపారుదల అవసరం",
        "no_irrigate": "✅ నీటిపారుదల అవసరం లేదు",
        "score_today": "ఈరోజు నీటి ఆప్టిమైజేషన్ స్కోర్",
        "score_yest": "నిన్నటి నీటి ఆప్టిమైజేషన్ స్కోర్",
        "compare": "📊 ఈరోజు vs నిన్న",
        "explain": "🧠 AI వివరణ"
    },

    "Malayalam": {
        "title": "🌱 AI അടിസ്ഥാനത്തിലുള്ള സ്മാർട്ട് ജലസേചന സംവിധാനം",
        "subtitle": "മഴയെ ആശ്രയിക്കുന്ന കൃഷിക്ക് റിയൽ-ടൈം AI പിന്തുണ",
        "select_city": "📍 നിങ്ങളുടെ നഗരം തിരഞ്ഞെടുക്കുക",
        "select_crop": "🌾 വിള തിരഞ്ഞെടുക്കുക",
        "weather": "🌦 തത്സമയ കാലാവസ്ഥ വിവരങ്ങൾ",
        "temp": "താപനില",
        "humidity": "ആർദ്രത",
        "rain": "കഴിഞ്ഞ 1 മണിക്കൂറിലെ മഴ",
        "map": "🗺 ഫാം ലൊക്കേഷൻ മാപ്പ്",
        "recommend": "🤖 AI ശുപാർശ",
        "irrigate": "💦 ജലസേചനം ആവശ്യമാണ്",
        "no_irrigate": "✅ ജലസേചനം ആവശ്യമില്ല",
        "score_today": "ഇന്നത്തെ ജല ഒപ്റ്റിമൈസേഷൻ സ്കോർ",
        "score_yest": "ഇന്നലെ ജല ഒപ്റ്റിമൈസേഷൻ സ്കോർ",
        "compare": "📊 ഇന്ന് vs ഇന്നലെ",
        "explain": "🧠 AI വിശദീകരണം"
    },

    "Kannada": {
        "title": "🌱 AI ಆಧಾರಿತ ಸ್ಮಾರ್ಟ್ ನೀರಾವರಿ ವ್ಯವಸ್ಥೆ",
        "subtitle": "ಮಳೆಯಾಧಾರಿತ ಕೃಷಿಗಾಗಿ ರಿಯಲ್-ಟೈಮ್ AI ನಿರ್ಧಾರ ಸಹಾಯ",
        "select_city": "📍 ನಿಮ್ಮ ನಗರವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "select_crop": "🌾 ಬೆಳೆ ಆಯ್ಕೆಮಾಡಿ",
        "weather": "🌦 ನೇರ ಹವಾಮಾನ ಮಾಹಿತಿ",
        "temp": "ತಾಪಮಾನ",
        "humidity": "ಆದ್ರತೆ",
        "rain": "ಕೊನೆಯ 1 ಗಂಟೆಯ ಮಳೆ",
        "map": "🗺 ಕೃಷಿ ಸ್ಥಳ ನಕ್ಷೆ",
        "recommend": "🤖 AI ಶಿಫಾರಸು",
        "irrigate": "💦 ನೀರಾವರಿ ಅಗತ್ಯ",
        "no_irrigate": "✅ ನೀರಾವರಿ ಅಗತ್ಯವಿಲ್ಲ",
        "score_today": "ಇಂದಿನ ನೀರಿನ ಆಪ್ಟಿಮೈಸೇಶನ್ ಅಂಕ",
        "score_yest": "ನಿನ್ನೆದಿನದ ನೀರಿನ ಆಪ್ಟಿಮೈಸೇಶನ್ ಅಂಕ",
        "compare": "📊 ಇಂದು ಮತ್ತು ನಿನ್ನೆ ಹೋಲಿಕೆ",
        "explain": "🧠 AI ವಿವರಣೆ"
    }
}

# ---------------- LANGUAGE SELECT ----------------
language = st.sidebar.selectbox("🌍 Language", list(translations.keys()))
t = translations[language]

# ---------------- TITLE ----------------
st.title(t["title"])
st.write(t["subtitle"])
st.markdown("---")

# ---------------- INPUT ----------------
city = st.selectbox(
    t["select_city"],
    ["Chennai,IN", "Coimbatore,IN", "Madurai,IN", "Salem,IN",
     "Virudhunagar,IN", "Bangalore,IN", "Hyderabad,IN", "Mumbai,IN"]
)

crop = st.selectbox(t["select_crop"], ["Rice", "Wheat", "Maize"])

# ---------------- WEATHER API ----------------
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
response = requests.get(url)
data = response.json()

if data.get("cod") != 200:
    st.error("Weather API Error. Check API Key.")
    st.stop()

temperature = data["main"]["temp"]
humidity = data["main"]["humidity"]
rainfall = data.get("rain", {}).get("1h", 0)

# ---------------- WEATHER DISPLAY ----------------
st.subheader(t["weather"])
st.write(f"🌡 {t['temp']}: **{temperature} °C**")
st.write(f"💧 {t['humidity']}: **{humidity}%**")
st.write(f"🌧 {t['rain']}: **{rainfall} mm**")

st.markdown("---")

# ---------------- MAP ----------------
coords = {
    "Chennai,IN": [13.0827, 80.2707],
    "Coimbatore,IN": [11.0168, 76.9558],
    "Madurai,IN": [9.9252, 78.1198],
    "Salem,IN": [11.6643, 78.1460],
    "Virudhunagar,IN": [9.5884, 77.9574],
    "Bangalore,IN": [12.9716, 77.5946],
    "Hyderabad,IN": [17.3850, 78.4867],
    "Mumbai,IN": [19.0760, 72.8777]
}

df_map = pd.DataFrame({"lat": [coords[city][0]], "lon": [coords[city][1]]})
st.subheader(t["map"])
st.map(df_map)

st.markdown("---")

# ---------------- AI LOGIC ----------------
threshold = {"Rice": 5, "Wheat": 3, "Maize": 2}[crop]
irrigation_needed = rainfall < threshold

today_score = max(20, int(100 - (rainfall * 10) - (humidity * 0.3)))
yesterday_score = max(20, today_score - 5)

# ---------------- RECOMMENDATION ----------------
st.subheader(t["recommend"])

if irrigation_needed:
    st.error(t["irrigate"])
else:
    st.success(t["no_irrigate"])

st.progress(today_score / 100)

st.write(f"{t['score_today']}: **{today_score}%**")
st.write(f"{t['score_yest']}: **{yesterday_score}%**")

st.markdown("---")

# ---------------- COMPARISON ----------------
st.subheader(t["compare"])

df = pd.DataFrame({
    "Day": ["Yesterday", "Today"],
    "Score": [yesterday_score, today_score]
})
st.bar_chart(df.set_index("Day"))

st.markdown("---")

# ---------------- AI EXPLANATION ----------------
st.subheader(t["explain"])

if irrigation_needed:
    st.write("AI detected low rainfall and crop water requirement. Irrigation is recommended to maintain soil moisture and improve yield.")
else:
    st.write("Sufficient rainfall detected. Irrigation can be postponed to conserve water resources.")

st.markdown("---")
st.caption("AI-powered irrigation system | Fully Multilingual Hackathon Version 🚀")
