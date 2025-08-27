
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

st.set_page_config(page_title='AI Virtual Fitness Coach', layout='wide')
st.title('AI Virtual Fitness Coach — Basic Rule-Based Demo')

BASE_DIR = Path(__file__).resolve().parent
data_dir = BASE_DIR / 'data'

# Load sample datasets
df_workouts = pd.read_csv(data_dir / 'workouts.csv')
df_meals = pd.read_csv(data_dir / 'nutrition.csv')

# Sidebar - user inputs
st.sidebar.header('Your profile')
age = st.sidebar.number_input('Age', min_value=12, max_value=90, value=25)
gender = st.sidebar.selectbox('Gender', ['Male', 'Female', 'Other'])
weight = st.sidebar.number_input('Weight (kg)', min_value=30.0, max_value=200.0, value=70.0)
height = st.sidebar.number_input('Height (cm)', min_value=120.0, max_value=230.0, value=175.0)
goal = st.sidebar.selectbox('Fitness Goal', ['Weight Loss', 'Muscle Gain', 'General Fitness'])
activity = st.sidebar.selectbox('Activity Level', ['Sedentary', 'Light', 'Moderate', 'Active'])
days_per_week = st.sidebar.slider('Days per week to train', 1, 7, 4)

# Helper functions
def compute_bmi(w, h_cm):
    h_m = h_cm / 100.0
    return w / (h_m * h_m)

def bmr_mifflin(age, weight, height, gender):
    # Mifflin-St Jeor Equation
    if gender.lower().startswith('m'):
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    return bmr

activity_factors = {'Sedentary': 1.2, 'Light': 1.375, 'Moderate': 1.55, 'Active': 1.725}

bmi = compute_bmi(weight, height)
bmr = bmr_mifflin(age, weight, height, gender)
maintenance_calories = int(bmr * activity_factors[activity])

if goal == 'Weight Loss':
    calorie_target = max(1200, maintenance_calories - 500)
elif goal == 'Muscle Gain':
    calorie_target = maintenance_calories + 300
else:
    calorie_target = maintenance_calories

# Show summary
st.subheader('Profile Summary')
col1, col2, col3 = st.columns(3)
col1.metric('BMI', f"{bmi:.1f}")
col2.metric('Maintenance Calories', f"{maintenance_calories} kcal")
col3.metric('Target Calories', f"{calorie_target} kcal")


# Workout plan (rule-based): pick top exercises for the goal
st.subheader('Suggested Workout Plan')
workouts = df_workouts[df_workouts['target'] == goal].reset_index(drop=True)
# choose N exercises based on days_per_week (simple rule)
n_ex = min(5, max(3, days_per_week))
selected = workouts.head(n_ex)
selected = selected[['exercise', 'category', 'duration_mins', 'reps_or_time', 'description']]
st.table(selected)

# Diet plan (simple selection)
st.subheader('Sample Diet Plan')
# pick one meal for each meal_type
meals_goal = df_meals[df_meals['goal'] == goal]
breakfast = meals_goal[meals_goal['meal_type'] == 'Breakfast'].sample(n=1, random_state=1).iloc[0]
lunch = meals_goal[meals_goal['meal_type'] == 'Lunch'].sample(n=1, random_state=2).iloc[0]
snack = meals_goal[meals_goal['meal_type'] == 'Snack'].sample(n=1, random_state=3).iloc[0]
dinner = meals_goal[meals_goal['meal_type'] == 'Dinner'].sample(n=1, random_state=4).iloc[0]

df_plan = pd.DataFrame([breakfast, lunch, snack, dinner])[['meal_type', 'meal', 'calories', 'protein_g', 'carbs_g', 'fats_g', 'items']]
df_plan = df_plan.rename(columns={'meal_type': 'Meal Type'})
total_cal = df_plan['calories'].sum()
st.table(df_plan)
st.write(f"Total sample calories (sum of meals shown): {int(total_cal)} kcal")
st.info('Note: This is a simple sample plan. For production, build a meal-assembly algorithm that matches target calories.')

# Quick training plan summary
st.subheader('Weekly Training Plan (example)')
st.write(f"Train {days_per_week} days/week. Example split:")
if goal == 'Muscle Gain':
    st.write('- Day 1: Upper Body (Strength)\n- Day 2: Lower Body (Strength)\n- Day 3: Rest or Light Cardio\n- Day 4: Full Body Strength\n- Day 5: Active Recovery/Yoga')
elif goal == 'Weight Loss':
    st.write('- Alternate cardio + HIIT + strength: e.g., Cardio, Strength, HIIT, Rest, Cardio')
else:
    st.write('- Mix of strength, cardio & mobility across the week. Include yoga or stretching.')

st.markdown('---')
st.caption('Built with sample CSVs. Next: integrate Mediapipe for pose detection and real-time rep counting.')
