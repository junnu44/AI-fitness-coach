# 🏋️ AI Fitness Coach — Project Report

## 1. Abstract
The **AI Fitness Coach** is a Flask-based web application that provides **personalized workout and nutrition recommendations**.  
The system takes user inputs such as **age, sex, weight, height, activity level, and fitness goal**, and then generates customized **meal plans and exercise routines**.  
It combines rule-based personalization, calorie/macro calculation, and datasets of workouts/nutrition to create an interactive, user-friendly platform.

---

## 2. Motivation
With rising awareness of health and fitness, individuals are looking for **personalized coaching solutions** without hiring expensive trainers.  
Most fitness apps require subscriptions and lack transparency.  
This project aims to:
- Offer **free, customizable plans**.
- Show how **data-driven approaches** can improve fitness recommendations.
- Build a **real-world project** using Flask, Pandas, and modern web UI.

---

## 3. System Architecture
The system is divided into the following components:

- **Frontend (UI Layer)**  
  - HTML, CSS (Glassmorphism design), Chart.js for visualizing macros.
  - Input form for user profile (age, weight, height, goal).
  - Results page showing recommended **workouts + meal plan**.

- **Backend (Flask Server)**  
  - Handles user input and routes (`/` for input, `/recommend` for output).
  - Calculates **BMR (Basal Metabolic Rate)** and **TDEE (Total Daily Energy Expenditure)** using the Mifflin-St Jeor formula.
  - Matches calorie/macro needs with available meals from dataset.
  - Selects workouts based on the user’s **fitness goal**.

- **Datasets (CSV Files)**  
  - `workouts.csv`: List of exercises with target category, duration, and description.  
  - `nutrition.csv`: Meal dataset with calories, macros, and target suitability.

- **Future ML Integration (Planned)**  
  - A model can be trained on user logs to optimize recommendations over time.

---

## 4. Implementation
1. **Input Collection**  
   User provides: age, sex, weight, height, activity level, fitness goal, and training frequency.

2. **Calorie & Macro Calculation**  
   - **BMR Formula**:  
     `BMR = 10*weight + 6.25*height - 5*age + [5 for male / -161 for female]`  
   - TDEE = BMR × Activity Multiplier  
   - Goal-based adjustments:  
     - Weight Loss → TDEE – 500  
     - Muscle Gain → TDEE + 300  
     - General Fitness → TDEE  

   Macro Split:  
   - Protein = 1.6 × body weight (grams)  
   - Fats = 25% of total calories  
   - Carbs = remaining calories  

3. **Workout Recommendation**  
   - Workouts filtered by target goal.  
   - Random selection of exercises (with safe sampling).  
   - Each workout has **duration, reps, description**.

4. **Nutrition Recommendation**  
   - Meals filtered by goal and meal type.  
   - Balanced plan for Breakfast, Lunch, Snack, Dinner.  
   - Adjusts snacks to meet calorie goals.

5. **UI & Visualization**  
   - Results displayed with clean UI cards.  
   - **Pie chart for macros** using Chart.js.  
   - Responsive design (desktop & mobile).

---

## 5. Results
- Users get **instant personalized plans** based on their profile.  
- Output includes:
  - Daily calorie & macro breakdown.  
  - Workout schedule (goal-specific).  
  - Balanced meals with calorie and macro values.  
- Example Screens:
  - Input form (user profile).  
  - Result dashboard with workouts + meals.  

---

## 6. Future Enhancements
- ✅ Add **Machine Learning model** for smarter recommendations.  
- ✅ Enable **user authentication** to track progress.  
- ✅ Store logs in **database (SQLite/Postgres)**.  
- ✅ Add **progress charts** for weight & performance.  
- ✅ Deploy on **Render / Heroku / AWS** for public use.  
- ✅ Mobile App version (React Native/Flutter).

---

## 7. Conclusion
The AI Fitness Coach demonstrates how **data-driven applications** can provide practical solutions in fitness.  
Using Flask, Pandas, and clean UI design, the project delivers **personalized, actionable plans**.  
With ML and deployment enhancements, it has potential to evolve into a **full-fledged fitness SaaS product**.

---

## 8. References
- Mifflin-St Jeor Equation for BMR  
- Fitness & Nutrition Science Resources  
- Flask & Pandas Documentation  
- Chart.js Visualization Library  

---
