from flask import Flask, render_template, request, send_from_directory
import pandas as pd
import os, math
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

app = Flask(__name__, static_folder="static", template_folder="templates")

# Load datasets
workouts = pd.read_csv(DATA_DIR / "workouts.csv")
nutrition = pd.read_csv(DATA_DIR / "nutrition.csv")

activity_multipliers = {
    "Sedentary": 1.2,
    "Light": 1.375,
    "Moderate": 1.55,
    "Active": 1.725
}

def calc_bmr(age, sex, weight, height):
    # Mifflin-St Jeor
    if sex.lower().startswith("m"):
        return 10*weight + 6.25*height - 5*age + 5
    else:
        return 10*weight + 6.25*height - 5*age - 161

def recommend_meals(target_cal, goal):
    # pick one meal per meal_type for given goal; attempt to match calories
    df = nutrition[nutrition["target"].str.lower() == goal.lower()]
    if df.empty:
        df = nutrition.copy()
    plan = []
    for meal_type in ["Breakfast","Lunch","Snack","Dinner"]:
        subset = df[df["meal_type"] == meal_type]
        if subset.empty:
            subset = nutrition[nutrition["meal_type"] == meal_type]
        if not subset.empty:
            plan.append(subset.sample(n=1, random_state=7).iloc[0].to_dict())
    # if total calories < target, try to top-up with extra snacks
    total = sum([m["calories"] for m in plan])
    snacks = df[df["meal_type"] == "Snack"]
    i = 0
    while total < target_cal - 300 and not snacks.empty and i < 5:
        s = snacks.sample(n=1, random_state=10+i).iloc[0].to_dict()
        plan.append(s)
        total += s["calories"]
        i += 1
    return plan, total

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    age = int(request.form.get("age", 25))
    sex = request.form.get("sex", "Male")
    weight = float(request.form.get("weight", 70))
    height = float(request.form.get("height", 170))
    activity = request.form.get("activity", "Moderate")
    goal = request.form.get("goal", "General Fitness")

    bmr = calc_bmr(age, sex, weight, height)
    tdee = int(bmr * activity_multipliers.get(activity, 1.55))

    if goal.lower() == "weight loss":
        target_cal = max(1200, tdee - 500)
    elif goal.lower() == "muscle gain":
        target_cal = tdee + 300
    else:
        target_cal = tdee

    # simple macro split
    protein_g = round(1.6 * weight)
    protein_cal = protein_g * 4
    fat_cal = 0.25 * target_cal
    fat_g = round(fat_cal / 9)
    remaining = target_cal - protein_cal - fat_cal
    carbs_g = max(0, round(remaining / 4))

    # workouts selection
    w_df = workouts[workouts["target"].str.lower() == goal.lower()]
    if w_df.empty:
        w_df = workouts.copy()
    n_ex = min(6, max(3, int(request.form.get("days_per_week", 4))))
    n_ex = min(n_ex, len(w_df))  # prevent sampling more than available
    selected_workouts = w_df.sample(n=n_ex, random_state=5).to_dict(orient="records")


    meal_plan, total_cal = recommend_meals(target_cal, goal)

    result = {
        "age": age, "sex": sex, "weight": weight, "height": height,
        "activity": activity, "goal": goal,
        "bmr": int(round(bmr)), "tdee": tdee, "target_cal": target_cal,
        "protein_g": protein_g, "carbs_g": carbs_g, "fat_g": fat_g,
        "workouts": selected_workouts, "meals": meal_plan, "total_meal_cal": int(total_cal)
    }
    return render_template("result.html", result=result)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(BASE_DIR / "static", filename)

if __name__ == "__main__":
    app.run(debug=True)