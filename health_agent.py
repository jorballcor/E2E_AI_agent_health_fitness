import streamlit as st
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_API_KEY = os.getenv("HF_API_TOKEN") 
MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"

client = InferenceClient(model=MODEL_NAME, token=HF_API_KEY)

for key, value in {
    "plans_generated": False,
    "dietary_plan": {},
    "fitness_plan": {},
    "qa_pairs": []
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.set_page_config(
    page_title="AI Health & Fitness Planner",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def generate_response(prompt):
    return client.text_generation(prompt, max_new_tokens=512).strip()

def generate_dietary_plan(user_profile):
    prompt = f"""
    You are a dietary expert. Based on the following user profile, provide a structured dietary plan.
    Profile:
    {user_profile}

    Your response should include:
    - Why this plan works
    - A detailed meal plan (breakfast, lunch, dinner, snacks)
    - Important dietary considerations
    """
    return generate_response(prompt)

def generate_fitness_plan(user_profile):
    prompt = f"""
    You are a fitness expert. Based on the following user profile, provide a structured workout plan.
    Profile:
    {user_profile}

    Your response should include:
    - The user's fitness goals
    - A structured exercise routine (warm-up, main workout, cool-down)
    - Pro tips for training
    """
    return generate_response(prompt)

def display_dietary_plan(plan_content):
    with st.expander("📋 Your Personalized Dietary Plan", expanded=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎯 Why this plan works")
            st.info(plan_content.get("why_this_plan_works", "Information not available"))
            st.markdown("### 🍽️ Meal Plan")
            st.write(plan_content.get("meal_plan", "Plan not available"))
        
        with col2:
            st.markdown("### ⚠️ Important Considerations")
            considerations = plan_content.get("important_considerations", "").split('\n')
            for consideration in considerations:
                if consideration.strip():
                    st.warning(consideration)

def display_fitness_plan(plan_content):
    with st.expander("💪 Your Personalized Fitness Plan", expanded=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎯 Goals")
            st.success(plan_content.get("goals", "Goals not specified"))
            st.markdown("### 🏋️‍♂️ Exercise Routine")
            st.write(plan_content.get("routine", "Routine not available"))
        
        with col2:
            st.markdown("### 💡 Pro Tips")
            tips = plan_content.get("tips", "").split('\n')
            for tip in tips:
                if tip.strip():
                    st.info(tip)

def main():
    st.title("🏋️‍♂️ AI Health & Fitness Planner")
    st.markdown("""
    <div style='background-color: #1E3A8A; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; color: white; text-align: center;'>
        <b>Get personalized dietary and fitness plans tailored to your goals and preferences.</b><br>
        Our AI-powered system considers your unique profile to create the perfect plan for you.
    </div>
""", unsafe_allow_html=True)


    st.header("👤 Your Profile")

    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=10, max_value=100, step=1, help="Enter your age")
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, step=0.1)
        activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"])
        dietary_preferences = st.selectbox("Dietary Preferences", ["Vegetarian", "Keto", "Gluten Free", "Low Carb", "Dairy Free"])

    with col2:
        weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, step=0.1)
        sex = st.selectbox("Sex", ["Male", "Female", "Other"])
        fitness_goals = st.selectbox("Fitness Goals", ["Lose Weight", "Gain Muscle", "Endurance", "Stay Fit", "Strength Training"])

    if st.button("🎯 Generate My Personalized Plan"):
        with st.spinner("Creating your health and fitness routine..."):
            user_profile = f"""
            Age: {age}
            Weight: {weight}kg
            Height: {height}cm
            Sex: {sex}
            Activity Level: {activity_level}
            Dietary Preferences: {dietary_preferences}
            Fitness Goals: {fitness_goals}
            """

            dietary_plan = {
                "why_this_plan_works": "High Protein, Healthy Fats, Moderate Carbohydrates, and Caloric Balance",
                "meal_plan": generate_dietary_plan(user_profile),
                "important_considerations": """
                - Hydration: Drink plenty of water throughout the day
                - Electrolytes: Monitor sodium, potassium, and magnesium levels
                - Fiber: Ensure adequate intake through vegetables and fruits
                - Listen to your body: Adjust portion sizes as needed
                """
            }

            fitness_plan = {
                "goals": "Build strength, improve endurance, and maintain overall fitness",
                "routine": generate_fitness_plan(user_profile),  
                "tips": """
                - Track your progress regularly
                - Allow proper rest between workouts
                - Focus on proper form
                - Stay consistent with your routine
                """
            }

            st.session_state.dietary_plan = dietary_plan
            st.session_state.fitness_plan = fitness_plan
            st.session_state.plans_generated = True

            display_dietary_plan(dietary_plan)
            display_fitness_plan(fitness_plan)

if __name__ == "__main__":
    main()
