import streamlit as st
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import re

# ---------- Admin Config ----------
ADMIN_PASSWORD = "Admin160622"
ADMIN_USERNAME = "ADMIN"

st.set_page_config(page_title="Health Assistant App", layout="centered")

st.title("💪 Health Assistant App")
st.write("Welcome! Choose a tool from the sidebar.")

tool = st.sidebar.selectbox(
    "Choose a tool", 
    [
        "Ideal Body Weight Calculator",
        "Exercise Planner",
        "Nutrition Analyzer",
        "Symptom Checker",
        "📊 Health Charts",
    ] + (["📬 View Feedback"] if st.session_state.get("is_admin") else [])
)

def height_to_inches(height_str):
    try:
        if "'" in height_str:
            feet, inches = height_str.split("'")
            inches = inches.replace('"', '').strip()
            return int(feet) * 12 + int(inches)
        elif "ft" in height_str:
            parts = height_str.lower().replace("in", "").split("ft")
            feet = int(parts[0].strip())
            inches = int(parts[1].strip()) if len(parts) > 1 else 0
            return feet * 12 + inches
    except:
        return None

def convert_height_to_cm(height_str):
    feet = 0
    inches = 0
    match1 = re.match(r"(\d+)'(\d+)", height_str)
    match2 = re.match(r"(\d+)\s*ft\s*(\d*)\s*in*", height_str)
    if match1:
        feet = int(match1.group(1))
        inches = int(match1.group(2))
    elif match2:
        feet = int(match2.group(1))
        inches = int(match2.group(2)) if match2.group(2) else 0
    else:
        return None
    total_inches = feet * 12 + inches
    return round(total_inches * 2.54, 2)

# Session defaults
if 'nutrition_score' not in st.session_state:
    st.session_state.nutrition_score = 0
if 'exercise_score' not in st.session_state:
    st.session_state.exercise_score = 0
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# Tools
if tool == "Ideal Body Weight Calculator":
    st.header("🏋️ Ideal Body Weight (IBW) Calculator")
    height_str = st.text_input("Enter your height (e.g., 5'7 or 5 ft 7 in)")
    gen = st.selectbox("Select your gender", options=["-- Select --", "male", "female"])
    if gen == "-- Select --":
        gen = None
    if st.button("Calculate IBW"):
        height_in = height_to_inches(height_str)
        if height_in is None:
            st.error("Please enter a valid height.")
        elif gen is None:
            st.error("Please select a gender.")
        else:
            base_height = 60
            ibw = 50 + 2.3 * (height_in - base_height) if gen == "male" else 45.5 + 2.3 * (height_in - base_height)
            st.success(f"Your Ideal Body Weight is approximately {ibw:.2f} kg")

elif tool == "Exercise Planner":
    st.header("🧘 Exercise Planner")
    age = st.number_input("Enter your age", min_value=1, max_value=120)
    gen = st.selectbox("Select your gender", options=["-- Select --", "male", "female"])
    if gen == "-- Select --":
        gen = None
    height_str = st.text_input("Enter your height (e.g., 5'7 or 5 ft 7 in)")
    weight = st.number_input("Enter your weight in kg", min_value=10.0, max_value=300.0)
    goal = st.selectbox("What's your fitness goal?", ["Weight Loss", "Muscle Gain", "General Fitness", "Flexibility & Stress Relief"])
    if st.button("Get Plan"):
        height_in = height_to_inches(height_str)
        if height_in is None or gen is None:
            st.error("Please enter valid height and gender.")
        else:
            st.success("Here’s your recommended fitness plan:")
            plans = {
                "Weight Loss": "- Cardio 5x/week\n- Strength 2–3x/week\n- Sleep 7–8 hrs\n- Hydration: 2.5–3L",
                "Muscle Gain": "- Strength 4–5x/week\n- Protein: dal, eggs, sprouts\n- Light cardio\n- Sleep 8 hrs",
                "General Fitness": "- Mix of cardio + strength + yoga 3–4x/week\n- Local grains & pulses",
                "Flexibility & Stress Relief": "- Yoga, breathing, walks\n- Meditation, stretching"
            }
            st.markdown(plans[goal])
            st.session_state.exercise_score = 25

elif tool == "Nutrition Analyzer":
    st.header("🍽️ Nutrition Analyzer")
    age = st.number_input("Enter your age", min_value=1, max_value=120)
    gen = st.selectbox("Select your gender", options=["-- Select --", "male", "female"])
    height_str = st.text_input("Enter your height (e.g., 5'7 or 5 ft 7 in)")
    weight = st.number_input("Enter your weight in kg", min_value=10.0, max_value=300.0)
    diet_type = st.radio("Are you vegan or non-vegan?", ["non-vegan", "vegan"])
    if st.button("Analyze Diet Plan"):
        if gen == "-- Select --" or not height_str:
            st.error("Please fill all fields.")
        else:
            height_cm = convert_height_to_cm(height_str)
            if height_cm is None:
                st.error("Invalid height format.")
            else:
                bmr = 10 * weight + 6.25 * height_cm - 5 * age + (5 if gen == "male" else -161)
                caloric_needs = int(bmr * 1.2)
                st.success(f"Daily Caloric Need: **{caloric_needs} calories**")
                plans = {
                    "non-vegan": "- Breakfast: Poha + egg + milk\n- Lunch: Rice + fish + chicken\n- Dinner: Chapati + egg curry",
                    "vegan": "- Breakfast: Millet dosa + chutney\n- Lunch: Roti + paneer/mushroom\n- Dinner: Veg salad + sprouts"
                }
                st.subheader(f"{diet_type.title()} South Indian Diet Plan:")
                st.markdown(plans[diet_type])
                st.session_state.nutrition_score = 25

elif tool == "Symptom Checker":
    st.header("🤔 Symptom Checker")
    symptoms = ["headache", "fatigue", "cold", "fever", "vomiting", "dizziness", "dehydration", "diarrhea", "sunburn", "heat rash", "muscle cramps", "nausea", "sore throat"]
    info = {
        "headache": ("Dehydration", "Drink water and rest."),
        "fatigue": ("Lack of sleep", "Rest well."),
        "cold": ("Viral", "Fluids and rest."),
        "fever": ("Infection", "Paracetamol."),
        "vomiting": ("Food poisoning", "ORS, no solids."),
        "dizziness": ("Low BP", "Sit and hydrate."),
        "dehydration": ("Low fluids", "ORS, water."),
        "diarrhea": ("Contamination", "Rehydrate."),
        "sunburn": ("UV exposure", "Aloe vera."),
        "heat rash": ("Sweat glands", "Cool environment."),
        "muscle cramps": ("Overuse", "Stretch, hydrate."),
        "nausea": ("Indigestion", "Rest."),
        "sore throat": ("Infection", "Gargle.")
    }
    selected = st.multiselect("Select symptoms", symptoms)
    if selected:
        for sym in selected:
            cause, remedy = info.get(sym, ("Unknown", "See doctor"))
            st.write(f"**{sym.title()}**\nCause: {cause}\nSolution: {remedy}")
        symptom_score = max(50 - len(selected) * 5, 0)
        total = symptom_score + st.session_state.nutrition_score + st.session_state.exercise_score
        st.markdown("---")
        st.write(f"Symptom Score: {symptom_score}/50\nNutrition: {st.session_state.nutrition_score}/25\nExercise: {st.session_state.exercise_score}/25")
        st.success(f"✅ Wellness Score: {total}/100")

elif tool == "📬 View Feedback":
    st.header("🔐 Admin Login - View Feedback")
    password = st.text_input("Enter admin password", type="password")
    if password == ADMIN_PASSWORD:
        st.session_state.is_admin = True
        if os.path.exists("user_feedback.csv"):
            df = pd.read_csv("user_feedback.csv")
            st.success("Access granted!")
            st.dataframe(df)
        else:
            st.info("No feedback yet.")
    elif password:
        st.error("Incorrect password.")

elif tool == "📊 Health Charts":
    st.header("📊 Health Overview Charts")
    pie_data = [st.session_state.exercise_score, st.session_state.nutrition_score, 100 - st.session_state.exercise_score - st.session_state.nutrition_score]
    labels = ['Exercise', 'Nutrition', 'Other']
    fig1, ax1 = plt.subplots()
    ax1.pie(pie_data, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

    radar_labels = ["Exercise", "Nutrition", "Symptom"]
    radar_scores = [st.session_state.exercise_score/25, st.session_state.nutrition_score/25, 1]
    angles = np.linspace(0, 2 * np.pi, len(radar_labels), endpoint=False).tolist()
    radar_scores += radar_scores[:1]
    angles += angles[:1]
    fig2, ax2 = plt.subplots(subplot_kw={'projection': 'polar'})
    ax2.plot(angles, radar_scores, 'o-', linewidth=2)
    ax2.fill(angles, radar_scores, alpha=0.25)
    ax2.set_thetagrids(np.degrees(angles[:-1]), radar_labels)
    ax2.set_title("Health Radar Chart")
    st.pyplot(fig2)

with st.expander("💬 Submit Feedback"):
    st.subheader("We'd love your feedback!")
    name = st.text_input("Your Name (optional)")
    rating = st.slider("Rate your experience (1–5)", 1, 5, 3)
    comment = st.text_area("Your Comments")
    if st.button("Submit Feedback"):
        feedback_df = pd.DataFrame([[name, rating, comment]], columns=["Name", "Rating", "Comment"])
        if os.path.exists("user_feedback.csv"):
            feedback_df.to_csv("user_feedback.csv", mode='a', header=False, index=False)
        else:
            feedback_df.to_csv("user_feedback.csv", index=False)
        st.success("✅ Feedback submitted! Thank you!")

st.markdown(
    """
    <style>
        .stApp {
            overflow-x: hidden;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)
