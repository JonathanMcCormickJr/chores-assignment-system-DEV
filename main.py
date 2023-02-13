from flask import Flask, render_template, request, make_response
from datetime import datetime
import pytz
import random
import json
import jsonify

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
        "cleaning_cars",
        "pets_care"
    ]
    mode = get_mode()
    if request.method == "POST":
        # Handle receiving chores responses
        name = request.form['name_input']
        
        # Your code to process the form data goes here
        # Check if the data already exists in the JSON file
        try:
            with open('data/responses.json') as f:
                data = json.load(f)
                for response in data:
                    if response[0] == name:
                        return 'Name already exists'
        except json.JSONDecodeError:
            data = []  # If the JSON file is empty, we must add '[]' to fix the JSONDecodeError
        
        # Write the user's responses to a JSON file
        chore_data = [name]
        for chore in chores:
            importance = request.form.get(chore + '_importance_select')
            competence = request.form.get(chore + '_competence_select')
            comfort = request.form.get(chore + '_comfort_select')
        
            
            chore_data.append([chore, {
                "importance": importance,
                "competence": competence,
                "comfort": comfort
            }])
            
        data.append(chore_data)
        with open('data/responses.json', 'w') as f:
            json.dump(data, f, indent=4)

        message = "<h1>Thank you!</h1><p><b>Your form has been successfully submitted!</b></p><div>" + str(chore_data) + "</div>"
        return render_template('confirmation.html', mode=mode, message=message) # 'Thanks for submitting your survey!'

        
    
    

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

@app.route('/check_name', methods=['POST'])
def check_name():
    name = request.form['name_input']
    # check if the name exists in the database
    name_exists = False
    with open('data/responses.json') as f:
        data = json.load(f)
        for response in data:
            if response[0] == name:
                name_exists = True
    return jsonify({'name_exists': name_exists})
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)
