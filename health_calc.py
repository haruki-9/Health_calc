import streamlit as st
import requests
import json

st.set_page_config(page_title="Health Assistant App", layout="centered")

st.title("💪 Health Assistant App")
st.write("Welcome! Choose a tool from the sidebar.")

# Sidebar options
tool = st.sidebar.selectbox(
    "Choose a tool", 
    ["Ideal Body Weight Calculator", "Exercise Planner", "Nutrition Analyzer", "Symptom Checker"]
)
#comment
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

# Initialize scores
if 'nutrition_score' not in st.session_state:
    st.session_state.nutrition_score = 0
if 'exercise_score' not in st.session_state:
    st.session_state.exercise_score = 0

# Tool: Ideal Body Weight Calculator
if tool == "Ideal Body Weight Calculator":
    st.header("🏋️ Ideal Body Weight (IBW) Calculator")
    height_str = st.text_input("Enter your height (e.g., 5'7 or 5 ft 7 in)")

    gen = st.selectbox(
        "Select your gender",
        options=["-- Select --", "male", "female"]
    )
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
    st.header("🧫 Exercise Planner")

    age = st.number_input("Enter your age", min_value=1, max_value=120, step=1)

    gen = st.selectbox(
        "Select your gender",
        options=["-- Select --", "male", "female"]
    )
    if gen == "-- Select --":
        gen = None

    height_str = st.text_input("Enter your height (e.g., 5'7 or 5 ft 7 in)")
    weight = st.number_input("Enter your weight in kg", min_value=10.0, max_value=300.0, step=0.1)

    goal = st.selectbox("What's your fitness goal?", ["Weight Loss", "Muscle Gain", "General Fitness"])

    if st.button("Get Plan"):
        height_in = height_to_inches(height_str)
        if height_in is None:
            st.error("Please enter a valid height.")
        elif gen is None:
            st.error("Please select a gender.")
        else:
            plan = ""
            if goal == "Weight Loss":
                plan = "Focus on cardio (30–45 min/day), light strength training 2–3x/week, and a calorie deficit."
            elif goal == "Muscle Gain":
                plan = "Strength training 4–5x/week with progressive overload, eat protein-rich meals."
            else:
                plan = "Combine moderate cardio and full-body workouts 3–4x/week with a balanced diet."
            st.success("Here’s your plan:")
            st.write(plan)
            st.session_state.exercise_score = 25

# Tool: Nutrition Analyzer
elif tool == "Nutrition Analyzer":
    st.header("🍽️ Nutrition Analyzer")
    st.write("This tool estimates your caloric needs and offers a basic diet plan.")

    age = st.number_input("Enter your age", min_value=1, max_value=120, step=1)

    gen = st.selectbox(
        "Select your gender",
        options=["-- Select --", "male", "female"]
    )
    if gen == "-- Select --":
        gen = None

    height_str = st.text_input("Enter your height (e.g., 5'7 or 5 ft 7 in)")
    weight = st.number_input("Enter your weight in kg", min_value=10.0, max_value=300.0, step=0.1)

    diet_type = st.radio("Are you vegan or non-vegan?", ["non-vegan", "vegan"])

    if st.button("Analyze Diet Plan"):
        if gen is None:
            st.error("Please select a gender.")
        elif not height_str:
            st.error("Please enter your height.")
        else:
            st.success("Nutrition analysis complete!")

            caloric_needs = 2500 if gen == "male" else 2000
            st.write(f"Your daily caloric needs are approximately {caloric_needs} calories.")

            st.subheader(f"Here's a sample {diet_type} diet plan for you:")

            if diet_type == "non-vegan":
                st.markdown("""
                **Breakfast:**
                - Scrambled eggs with whole grain toast and mixed berries  
                - Greek yogurt with granola and honey

                **Lunch:**
                - Grilled chicken breast with brown rice and mixed vegetables  
                - Turkey and avocado wrap with mixed greens

                **Dinner:**
                - Grilled salmon with roasted vegetables and quinoa  
                - Chicken stir-fry with mixed vegetables and brown rice
                """)
            else:
                st.markdown("""
                **Breakfast:**
                - Oatmeal with almond milk, chia seeds, and banana  
                - Peanut butter on whole wheat toast with a fruit smoothie

                **Lunch:**
                - Chickpea curry with brown rice and spinach  
                - Tofu and veggie stir-fry with quinoa

                **Dinner:**
                - Lentil soup with multigrain bread and salad  
                - Grilled vegetables with millet and hummus
                """)

            st.session_state.nutrition_score = 25

# Tool: Symptom Checker
elif tool == "Symptom Checker":
    st.header("🤔 Symptom Checker")

    symptoms = [
        "headache", "fatigue", "cold", "fever", "vomiting",
        "dizziness", "dehydration", "diarrhea", "sunburn",
        "heat rash", "muscle cramps", "nausea", "sore throat"
    ]

    symptom_info = {
        "headache": ("Dehydration, stress, or screen fatigue", "Drink water, rest, reduce screen time."),
        "fatigue": ("Lack of sleep, anemia, or poor diet", "Get proper rest, eat iron-rich foods."),
        "cold": ("Viral infection or allergies", "Stay warm, take rest and drink fluids."),
        "fever": ("Infection or inflammation", "Use paracetamol, see doctor if persists."),
        "vomiting": ("Food poisoning or heat-related illness", "Use ORS, avoid solid food temporarily."),
        "dizziness": ("Low BP or dehydration", "Sit down, drink fluids."),
        "dehydration": ("Inadequate fluid intake", "Drink ORS and rest in cool place."),
        "diarrhea": ("Infection or contaminated food/water", "Hydrate with ORS, avoid oily food."),
        "sunburn": ("UV exposure", "Use aloe vera or cool compress."),
        "heat rash": ("Sweat gland blockage", "Keep area cool and dry."),
        "muscle cramps": ("Electrolyte imbalance or overuse", "Stretch and drink coconut water."),
        "nausea": ("Indigestion or heat stress", "Rest and sip fluids."),
        "sore throat": ("Viral infection or allergies", "Gargle with salt water, drink warm fluids.")
    }

    selected = st.multiselect("Select symptoms you are experiencing", symptoms)
    if selected:
        for sym in selected:
            cause, solution = symptom_info.get(sym, ("Unknown", "Consult a doctor."))
            st.subheader(sym.capitalize())
            st.write(f"**Cause:** {cause}")
            st.write(f"**Suggested Solution:** {solution}")

        max_symptom_score = 50
        symptom_score = max_symptom_score - len(selected) * 5
        symptom_score = max(symptom_score, 0)

        total_score = symptom_score + st.session_state.nutrition_score + st.session_state.exercise_score

        st.markdown("---")
        st.header("🌟 Your Overall Wellness Score")
        st.write(f"**Symptom Score:** {symptom_score}/50")
        st.write(f"**Nutrition Score:** {st.session_state.nutrition_score}/25")
        st.write(f"**Exercise Score:** {st.session_state.exercise_score}/25")
        st.success(f"✅ Your total Wellness Score is: **{total_score}/100**")

        st.info("This score combines symptoms, nutrition, and exercise data. Let us know if you'd like future versions to include sleep or mental health factors too!")
    else:
        st.info("Please select one or more symptoms to get insights.")
