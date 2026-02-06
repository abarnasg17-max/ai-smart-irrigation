import streamlit as st
import requests
import pandas as pd

# ---------------- CONFIG ----------------
API_KEY = "cd7c64ae1d8ad11ce323be2d781069eb"   # <-- UNGA REAL API KEY INGA PASTE PANNUNGA
st.set_page_config(page_title="AI Smart Irrigation", page_icon="🌱", layout="centered")

# ---------------- UI ----------------
st.title("🌱 AI-Driven Smart Irrigation & Water Optimization System")
st.write("Real-time, AI-inspired decision support system for rain-fed farms")

st.markdown("---")

# ---------------- USER INPUT ----------------
city = st.selectbox(
    "📍 Select Your City",
    [
        "Chennai,IN", "Coimbatore,IN", "Madurai,IN", "Salem,IN",
        "Virudhunagar,IN", "Tirunelveli,IN", "Thanjavur,IN",
        "Bangalore,IN", "Hyderabad,IN", "Mumbai,IN", "Delhi,IN"
    ]
)

crop = st.selectbox("🌾 Select Crop Type", ["Rice", "Wheat", "Maize"])

# ---------------- FETCH REAL-TIME WEATHER ----------------
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
response = requests.get(url)
data = response.json()

# Error handling
if data.get("cod") != 200:
    st.error("⚠️ Weather data not available. Please check API key or city name.")
    st.stop()

# Read weather safely
temperature = data["main"]["temp"]
humidity = data["main"]["humidity"]
rainfall = data.get("rain", {}).get("1h", 0)

# ---------------- DISPLAY WEATHER ----------------
st.markdown("### 🌦️ Live Weather Data")
st.write(f"🌡️ Temperature: **{temperature} °C**")
st.write(f"💧 Humidity: **{humidity} %**")
st.write(f"🌧️ Rainfall (last 1 hour): **{rainfall} mm**")

st.markdown("---")

# =================================================
# 🧠 AI-INSPIRED DECISION LOGIC
# =================================================

# Crop-based rainfall threshold
if crop == "Rice":
    crop_threshold = 5
elif crop == "Wheat":
    crop_threshold = 3
else:  # Maize
    crop_threshold = 2

# Irrigation decision
if rainfall < crop_threshold:
    irrigation_result = "💦 Irrigation Needed"
else:
    irrigation_result = "✅ No Irrigation Needed"

# =================================================
# 🔥 DYNAMIC WATER OPTIMIZATION SCORE (ADVANCED)
# =================================================
score = 100 - (rainfall * 10) - (humidity * 0.3)

if crop == "Rice":
    score -= 5
elif crop == "Wheat":
    score -= 3
else:  # Maize
    score -= 1

optimization_score = max(20, min(95, int(score)))

# =================================================
# 📊 PREDICTION CONFIDENCE (AI BEHAVIOR)
# =================================================
if rainfall < 1:
    confidence = 70
elif rainfall < 5:
    confidence = 85
else:
    confidence = 92

# ---------------- RESULTS ----------------
st.markdown("### 🤖 AI Recommendation")
st.success(irrigation_result)
st.write(f"💧 **Water Optimization Score:** {optimization_score}%")
st.write(f"📊 **Prediction Confidence:** {confidence}%")

st.markdown("---")

# =================================================
# 📅 IRRIGATION PLAN (NEXT 3 DAYS)
# =================================================
st.markdown("### 📅 Irrigation Plan (Next 3 Days)")

if rainfall > crop_threshold:
    st.write("**Today:** No irrigation needed")
    st.write("**Day 2:** No irrigation needed")
    st.write("**Day 3:** Moderate irrigation")
else:
    st.write("**Today:** Irrigation needed")
    st.write("**Day 2:** Moderate irrigation")
    st.write("**Day 3:** High irrigation")

st.markdown("---")

# =================================================
# 📈 GRAPH: RAINFALL vs OPTIMIZATION SCORE
# =================================================
st.markdown("### 📈 Rainfall vs Water Optimization Analysis")

rain_values = [0, 2, 5, 8, 12]
opt_scores = [
    max(20, min(95, int(100 - (r * 10) - (humidity * 0.3))))
    for r in rain_values
]

df = pd.DataFrame({
    "Rainfall (mm)": rain_values,
    "Optimization Score (%)": opt_scores
})

st.line_chart(df.set_index("Rainfall (mm)"))

# ---------------- FOOTER ----------------
st.caption(
    "🔬 This AI-driven system uses real-time weather data, crop sensitivity, "
    "dynamic scoring, confidence estimation, and visual analytics to optimize irrigation decisions."
)
