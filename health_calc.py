import streamlit as st

# --- Utility Functions ---

def calculate_ibw(height_cm, gen):
    if gen.lower() == 'male':
        base_weight = 50
    elif gen.lower() == 'female':
        base_weight = 45.5
    else:
        raise ValueError("Invalid Gender. Please enter 'male' or 'female'.")
    ibw = base_weight + 0.91 * (height_cm - 152.4)
    return round(ibw, 2)

def convert_height_to_cm(height_str):
    try:
        height_str = height_str.replace("'", " ").replace('"', "").replace("ft", " ").replace("in", " ")
        parts = height_str.split()
        feet = int(parts[0])
        inches = int(parts[1])
        return (feet * 12 + inches) * 2.54
    except:
        return None

def calculate_mhr(age):
    return 220 - age

# --- Symptom Checker Data ---

possible_symptoms = {
    "headache": {"cause": "Dehydration, stress, heat exposure, or underlying medical condition", "solution": "Drink water, rest, reduce screen time. If persistent, consult a doctor."},
    "fatigue": {"cause": "Lack of sleep, poor diet, anemia, dehydration, or heat exhaustion", "solution": "Get proper sleep, hydrate, eat well. If it continues, see a doctor."},
    "cold": {"cause": "Common cold virus, allergies, or sudden temperature changes", "solution": "Stay warm, rest, drink fluids. OTC meds may help."},
    "fever": {"cause": "Infection, heat stroke, or inflammatory condition", "solution": "Hydrate, use paracetamol. If high or lasts >2 days, see a doctor."},
    "vomiting": {"cause": "Food poisoning, stomach flu, or heat-related illness", "solution": "Use ORS, avoid solids briefly. Consult if >24 hours."},
    "dizziness": {"cause": "Low BP, dehydration, heat exhaustion, or anemia", "solution": "Sit/lie down, hydrate. Frequent episodes need a doctor."},
    "dehydration": {"cause": "Low fluid intake, sweating, or sun exposure", "solution": "Drink ORS, rest in shade. Severe = medical help."},
    "diarrhea": {"cause": "Food poisoning, bad water, or infection", "solution": "Hydrate with ORS, avoid oily food. >2 days = doctor."},
    "sunburn": {"cause": "Too much UV exposure", "solution": "Use aloe vera/lotion. Severe blisters? See doctor."},
    "heat rash": {"cause": "Blocked sweat glands", "solution": "Keep dry/cool, loose clothes, powder or mild steroid."},
    "muscle cramps": {"cause": "Electrolyte imbalance or overexertion", "solution": "Stretch, drink coconut water. Frequent? Medical review."},
    "nausea": {"cause": "Heat exhaustion, bad food, dehydration", "solution": "Rest, hydrate, avoid strong smells. If severe, see doctor."},
    "sore throat": {"cause": "Virus, dry air, or allergies", "solution": "Salt water gargle, herbal teas. >3 days = doctor."}
}

# --- Nutrition Analyzer ---

def nutrition_analyzer(age, gen, height_cm, weight_kg, diet_type):
    caloric_needs = 2500  # basic estimate
    st.write(f"### Your daily caloric needs: **{caloric_needs} calories**")
    if diet_type.lower() == "vegan":
        st.subheader("Sample Vegan Diet Plan")
        st.markdown("""
        **Breakfast:**  
        - Oatmeal with almond milk, banana, and walnuts  
        - Whole grain toast with avocado and cherry tomatoes
        **Lunch:**  
        - Lentil soup with whole grain bread  
        - Quinoa salad with roasted vegetables and chickpeas
        **Dinner:**  
        - Vegan stir-fry with tofu, vegetables, and brown rice  
        - Grilled portobello mushrooms with quinoa
        """)
    elif diet_type.lower() == "non-vegan":
        st.subheader("Sample Non-Vegan Diet Plan")
        st.markdown("""
        **Breakfast:**  
        - Scrambled eggs with whole grain toast and berries  
        - Greek yogurt with granola and honey
        **Lunch:**  
        - Grilled chicken with brown rice and veggies  
        - Turkey and avocado wrap
        **Dinner:**  
        - Grilled salmon with quinoa and vegetables  
        - Chicken stir-fry with rice
        """)
    else:
        st.error("Invalid diet type. Please choose vegan or non-vegan.")

# --- Exercise Planner ---

def get_exercise_plan(goal, age, height_cm, weight_kg):
    if goal == "Weight Loss":
        return """
        **Recommended Plan (Weight Loss):**
        - **Cardio**: 30–45 min brisk walk/jog, 5 days/week  
        - **Strength**: Light resistance training, 3 days/week  
        - **Flexibility**: Yoga/stretching, 3 days/week  
        - **Tips**: Calorie deficit, hydrate well
        """
    elif goal == "Gain Mass":
        return """
        **Recommended Plan (Gain Mass):**
        - **Strength**: Heavy lifting, compound exercises (4–5x/week)  
        - **Cardio**: Light, 2x/week to maintain health  
        - **Diet**: Caloric surplus, high protein  
        - **Tips**: Track progress weekly
        """
    elif goal == "Improve Muscle Tone":
        return """
        **Recommended Plan (Muscle Tone):**
        - **Strength**: Moderate weights, high reps (4x/week)  
        - **Cardio**: HIIT 2–3x/week  
        - **Flexibility**: Foam rolling, stretching post-workout  
        - **Tips**: Consistency over intensity
        """
    else:
        return "**Invalid Goal**"

# --- Streamlit App UI ---

st.title("🩺 Health Assistant App")
st.markdown("Welcome! Choose a tool from the sidebar.")

option = st.sidebar.selectbox(
    "Choose a Tool",
    [
        "Ideal Body Weight Calculator",
        "Max Heart Rate Calculator",
        "Symptom Checker",
        "Nutrition Analyzer",
        "Exercise Planner"  # <-- NEW SECTION
    ]
)

if option == "Ideal Body Weight Calculator":
    st.header("🏋️ Ideal Body Weight (IBW) Calculator")
    height_str = st.text_input("Enter your height (e.g., 5'7 or 5 ft 7 in)")
    gen = st.radio("Select your gender", ["male", "female"])
    if st.button("Calculate IBW"):
        height_cm = convert_height_to_cm(height_str)
        if height_cm:
            ibw = calculate_ibw(height_cm, gen)
            st.success(f"Your height is: {height_cm:.2f} cm")
            st.success(f"Ideal Body Weight: **{ibw} kg**")
        else:
            st.error("Invalid height format.")

elif option == "Max Heart Rate Calculator":
    st.header("❤️ Max Heart Rate (MHR) Calculator")
    age = st.number_input("Enter your age", min_value=1, max_value=120, value=25)
    if st.button("Calculate MHR"):
        mhr = calculate_mhr(age)
        st.success(f"Your Maximum Heart Rate is **{mhr} bpm**")

elif option == "Symptom Checker":
    st.header("🔍 Symptom Checker")
    selected_symptoms = st.multiselect("Select your symptoms", list(possible_symptoms.keys()))
    if selected_symptoms:
        for symptom in selected_symptoms:
            data = possible_symptoms[symptom]
            st.subheader(f"🩺 {symptom.capitalize()}")
            st.write(f"**Cause:** {data['cause']}")
            st.write(f"**Solution:** {data['solution']}")
    else:
        st.info("Select at least one symptom to get results.")

elif option == "Nutrition Analyzer":
    st.header("🍽️ Nutrition Analyzer")
    age = st.number_input("Enter your age", min_value=1, max_value=120)
    gen = st.radio("Select your gender", ["male", "female"])
    height_str = st.text_input("Enter your height (e.g., 5'7 or 5 ft 7 in)")
    weight_kg = st.number_input("Enter your weight in kg", min_value=10.0, max_value=300.0)
    diet_type = st.selectbox("Choose your diet type", ["vegan", "non-vegan"])
    if st.button("Analyze Nutrition"):
        height_cm = convert_height_to_cm(height_str)
        if height_cm:
            nutrition_analyzer(age, gen, height_cm, weight_kg, diet_type)
        else:
            st.error("Invalid height format.")

elif option == "Exercise Planner":
    st.header("💪 Exercise Planner")
    age = st.number_input("Enter your age", min_value=1, max_value=120)
    height_str = st.text_input("Enter your height (e.g., 5'7 or 5 ft 7 in)")
    weight_kg = st.number_input("Enter your weight in kg", min_value=10.0, max_value=300.0)
    goal = st.selectbox("What's your fitness goal?", ["Weight Loss", "Gain Mass", "Improve Muscle Tone"])

    if st.button("Get Plan"):
        height_cm = convert_height_to_cm(height_str)
        if height_cm:
            plan = get_exercise_plan(goal, age, height_cm, weight_kg)
            st.success("✅ Here's your exercise plan:")
            st.markdown(plan)
        else:
            st.error("Invalid height format. Please use format like 5'7 or 5 ft 7 in.")
