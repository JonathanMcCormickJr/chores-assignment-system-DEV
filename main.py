from flask import Flask, render_template, request
from datetime import datetime
import pytz
import random
import json

app = Flask(__name__)
app.debug = True


# DARK MODE AUTO-ASSIGN

def get_mode():
    

    def is_nighttime():
        new_hampshire_tz = pytz.timezone('America/New_York')
        now = datetime.now(new_hampshire_tz)
        current_time_nh = int(now.strftime("%H%M%S"))
        return not 60000 < current_time_nh < 180000  # Use IRL
        return 60000 < current_time_nh < 180000  # Use ONLY for testing

    if is_nighttime():
        return 'dark'
    else:
        return 'light'


# Pages

@app.route('/')
def index():
    mode = get_mode()
    return render_template('index.html', mode=mode)

@app.route("/about")
def about():
    mode = get_mode()
    return render_template("about.html", mode=mode)

@app.route("/analytics")
def analytics():
    mode = get_mode()
    return render_template("analytics.html", mode=mode)

@app.route("/survey", methods=['GET', 'POST'])
def survey():
    chores = [
        "kitchen",
        "sweeping",
        "laundry",
        "bathrooms",
        "trash",
        "mowing",
        "gardening",
        "cooking",
        "mirrors",
        "decluttering",
        "clening_cars",
        "pets_care"
    ]
    
    if request.method == "POST":
        # Handle receiving chores responses
        name = request.form['name_input']
        importance = request.form.getlist('importance_select')
        competence = request.form.getlist('competence_select')
        comfort = request.form.getlist('comfort_select')
        # Your code to process the form data goes here
        # Check if the data already exists in the JSON file
        with open('data/responses.json') as f:
            data = json.load(f)
            for response in data:
                if response["name"] == name:
                    return 'Name already exists'
        # Write the user's responses to a JSON file
        chores_data = {}
        for chore in chores:
            chore_reactions = "chore:[]"
            chores_data = chores_data.append(chore_reactions)
            
        new_response = [name, chores_data]
        
        data["responses"].append(new_response)
        
        with open('data/responses.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        return 'Thanks for submitting your survey!'

        # Delete this later
        user_text = request.form["text"]

        with open("text.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([user_text])

        return "Text saved!"
        
    mode = get_mode()
    

    # Stuff for DEBUGGING
    names             = ['Emma', 'Olivia', 'Ava', 'Isabella', 'Sophia', 'Mia', 'Charlotte', 'Amelia', 'Harper', 'Evelyn', 'Abigail', 'Emily', 'Elizabeth', 'Avery', 'Sofia', 'Ella', 'Madison', 'Scarlett', 'Victoria', 'Aria', 'Grace', 'Chloe', 'Camila', 'Penelope', 'Riley', 'Nora', 'Lily', 'Eleanor', 'Hazel', 'Aubrey']
    importance_levels = ['not_important', 'somewhat_important', 'important', 'very_important']
    competence_levels = ["cant_do_it", "need_help", "can_do_it_easily"]
    comfort_levels    = ["hate_it", "dont_like_it", "neutral", "like_it", "love_it"]
    # Handle sending chores list 
    if app.debug == True:
        return render_template('survey.html', mode=mode, chores=chores, DEBUG=app.debug, random_name=random.choice(names), random_importance=random.choice(importance_levels), random_competence=random.choice(competence_levels), random_comfort=random.choice(comfort_levels))
    else:
        return render_template('survey.html', mode=mode, chores=chores, DEBUG=app.debug)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)
