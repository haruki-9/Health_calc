import streamlit as st
import re
import requests
import json
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Health Assistant App", layout="centered")

st.title("💪 Health Assistant App")
st.write("Welcome! Choose a tool from the sidebar.")

# Sidebar options:-
tool = st.sidebar.selectbox(
    "Choose a tool", 
    [
        "Ideal Body Weight Calculator",
        "Exercise Planner",
        "Nutrition Analyzer",
        "Symptom Checker",
        "📊 Health Charts"
    ]
)

# Utility to convert height string to inches
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

# Utility to convert height to cm
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

# Initialize scores
if 'nutrition_score' not in st.session_state:
    st.session_state.nutrition_score = 0
if 'exercise_score' not in st.session_state:
    st.session_state.exercise_score = 0

# Tool: Ideal Body Weight Calculator
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
            if gen == "male":
                ibw = 50 + 2.3 * (height_in - base_height) if height_in > base_height else 50
            else:
                ibw = 45.5 + 2.3 * (height_in - base_height) if height_in > base_height else 45.5
            st.success(f"Your Ideal Body Weight is approximately {ibw:.2f} kg")

# Tool: Exercise Planner
elif tool == "Exercise Planner":
    st.header("🧘 Exercise Planner")
    age = st.number_input("Enter your age", min_value=1, max_value=120, step=1)
    gen = st.selectbox("Select your gender", options=["-- Select --", "male", "female"])
    if gen == "-- Select --":
        gen = None

    height_str = st.text_input("Enter your height (e.g., 5'7 or 5 ft 7 in)")
    weight = st.number_input("Enter your weight in kg", min_value=10.0, max_value=300.0, step=0.1)
    goal = st.selectbox("What's your fitness goal?", ["Weight Loss", "Muscle Gain", "General Fitness", "Flexibility & Stress Relief"])

    if st.button("Get Plan"):
        height_in = height_to_inches(height_str)
        if height_in is None:
            st.error("Please enter a valid height.")
        elif gen is None:
            st.error("Please select a gender.")
        else:
            st.success("Here’s your recommended fitness plan:")
            if goal == "Weight Loss":
                st.markdown("""
                - **Cardio:** 5 days/week – 30 to 45 minutes/session  
                - **Strength Training:** 2–3 days/week  
                - **Diet Tip:** Stay in calorie deficit.  
                - **Recovery:** 7–8 hours sleep, hydration (2.5–3 L/day)  
                """)
            elif goal == "Muscle Gain":
                st.markdown("""
                - **Strength Training:** 4–5 days/week  
                - **Protein Intake:** Include dal, paneer, eggs, chicken, sprouts  
                - **Rest & Recovery:** Sleep 8 hrs/night  
                - **Cardio:** Light cardio 2x/week  
                """)
            elif goal == "General Fitness":
                st.markdown("""
                - **Routine Mix:** Cardio + strength + flexibility (3–4x/week)  
                - **Examples:** Walking, yoga, home circuits  
                - **Diet:** Whole grains, local veggies, pulses  
                """)
            elif goal == "Flexibility & Stress Relief":
                st.markdown("""
                - **Yoga & Stretching:** 4–5x/week  
                - **Breathing & Meditation:** Daily  
                - **Supplemental:** Walks, music meditation  
                """)

            st.session_state.exercise_score = 25

# Tool: Nutrition Analyzer (updated)
elif tool == "Nutrition Analyzer":
    st.header("🍽️ Nutrition Analyzer")
    st.write("This tool estimates your daily caloric needs and suggests a South Indian-style diet plan.")

    age = st.number_input("Enter your age", min_value=1, max_value=120, step=1)
    gen = st.selectbox("Select your gender", options=["-- Select --", "male", "female"])
    height_str = st.text_input("Enter your height (e.g., 5'7 or 5 ft 7 in)")
    weight = st.number_input("Enter your weight in kg", min_value=10.0, max_value=300.0, step=0.1)
    diet_type = st.radio("Are you vegan or non-vegan?", ["non-vegan", "vegan"])

    if st.button("Analyze Diet Plan"):
        if gen == "-- Select --":
            st.error("Please select a gender.")
        elif not height_str:
            st.error("Please enter your height.")
        else:
            height_cm = convert_height_to_cm(height_str)
            if height_cm is None:
                st.error("Invalid height format. Please use formats like 5'7 or 5 ft 7 in.")
            else:
                if gen == "male":
                    bmr = 10 * weight + 6.25 * height_cm - 5 * age + 5
                else:
                    bmr = 10 * weight + 6.25 * height_cm - 5 * age - 161

                caloric_needs = int(bmr * 1.2)
                st.success("Nutrition analysis complete!")
                st.write(f"Your estimated daily caloric need is **{caloric_needs} calories**.")

                st.subheader(f"Here's a sample {diet_type} South Indian-style diet plan:")

                if diet_type == "non-vegan":
                    st.markdown("""
                    - **Breakfast:**  
                      - Boiled egg with poha  
                      - Banana with milk  
                    - **Lunch:**  
                      - Fish gravy with roti/rice  
                      - Chicken curry with chapati  
                    - **Dinner:**  
                      - Fish fry with chapati/pulka  
                      - Egg masala with jowar roti  
                    """)
                else:
                    st.markdown("""
                    - **Breakfast:**  
                      - Millet dosa with coconut chutney  
                      - Steamed vegetables with toasted paneer  
                    - **Lunch:**  
                      - Roti with lettuce, paneer, and mushroom curry  
                      - Brown rice with mixed dal curry  
                    - **Dinner:**  
                      - Steamed vegetables and steamed nuts  
                      - Salad with channa, rajma, and sprouts  
                    """)

                st.session_state.nutrition_score = 25

# Tool: Symptom Checker
elif tool == "Symptom Checker":
    st.header("🤔 Symptom Checker")
    symptoms = ["headache", "fatigue", "cold", "fever", "vomiting", "dizziness", "dehydration", "diarrhea", "sunburn", "heat rash", "muscle cramps", "nausea", "sore throat"]

    symptom_info = {
        "headache": ("Dehydration, stress", "Drink water, rest."),
        "fatigue": ("Lack of sleep", "Get proper rest."),
        "cold": ("Viral", "Take rest, drink fluids."),
        "fever": ("Infection", "Use paracetamol."),
        "vomiting": ("Food poisoning", "Use ORS, avoid solid food."),
        "dizziness": ("Low BP", "Sit down, drink fluids."),
        "dehydration": ("Low fluids", "Drink ORS."),
        "diarrhea": ("Contaminated food", "Hydrate."),
        "sunburn": ("UV exposure", "Use aloe vera."),
        "heat rash": ("Sweat glands", "Keep cool."),
        "muscle cramps": ("Overuse", "Stretch, hydrate."),
        "nausea": ("Indigestion", "Rest, sip fluids."),
        "sore throat": ("Infection", "Gargle, warm fluids.")
    }

    selected = st.multiselect("Select symptoms", symptoms)
    if selected:
        for sym in selected:
            cause, solution = symptom_info.get(sym, ("Unknown", "Consult a doctor."))
            st.subheader(sym.capitalize())
            st.write(f"**Cause:** {cause}")
            st.write(f"**Solution:** {solution}")

        symptom_score = max(50 - len(selected) * 5, 0)
        total_score = symptom_score + st.session_state.nutrition_score + st.session_state.exercise_score

        st.markdown("---")
        st.header("🌟 Your Overall Wellness Score")
        st.write(f"**Symptom Score:** {symptom_score}/50")
        st.write(f"**Nutrition Score:** {st.session_state.nutrition_score}/25")
        st.write(f"**Exercise Score:** {st.session_state.exercise_score}/25")
        st.success(f"✅ Total Score: {total_score}/100")

# Tool: Health Charts
elif tool == "📊 Health Charts":
    st.header("📊 Health Visualization")
    st.write("Here you can visualize your health progress across symptoms, nutrition, and exercise.")

    labels = ['Symptoms', 'Nutrition', 'Exercise']
    scores = [
        max(0, 50 - len(st.session_state.get('symptoms', [])) * 5) if 'symptoms' in st.session_state else 50,
        st.session_state.nutrition_score,
        st.session_state.exercise_score
    ]

    # Pie Chart
    st.subheader("🟠 Pie Chart")
    fig1, ax1 = plt.subplots()
    ax1.pie(scores, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

    # Radar Chart
    st.subheader("🕸️ Radar Chart")
    fig2 = plt.figure()
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    scores += scores[:1]
    angles += angles[:1]

    ax2 = fig2.add_subplot(111, polar=True)
    ax2.plot(angles, scores, 'o-', linewidth=2)
    ax2.fill(angles, scores, alpha=0.25)
    ax2.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax2.set_title("Wellness Radar Chart")
    ax2.grid(True)
    st.pyplot(fig2)
