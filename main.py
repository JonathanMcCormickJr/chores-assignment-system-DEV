from flask import Flask, render_template, request
from datetime import datetime
import pytz
import random
import json
import unittest

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

    with open('data/responses.json') as f:
        responses = json.load(f)
    
    scores = {}
    detailed_scores = {}
    for response in responses:
        person = response[0]
        score = 0
        for task in response[1:]:
            task_score = 0
            task_importance = task[1]["importance"]
            task_competence = task[1]["competence"]
            task_comfort = task[1]["comfort"]
            
            # Determine importance score
            importance_score = 0
            if task_importance == "not_important":
                importance_score = 0
            elif task_importance == "somewhat_important":
                importance_score = 1/3
            elif task_importance == "important":
                importance_score = 2/3
            elif task_importance == "very_important":
                importance_score = 1
            else: 
                return "error with calculating importance_score for " + person
            
            # Determine competence score "cant_do_it", "need_help", "can_do_it_easily"
            competence_score = 0
            if task_competence == "cant_do_it":
                competence_score = 0
            elif task_competence == "need_help":
                competence_score = 0.5
            elif task_competence == "can_do_it_easily":
                competence_score = 1
            else:
                return "error with calculating competence_score for " + person
                
            # Determine comfort score "hate_it", "dont_like_it", "neutral", "like_it", "love_it"
            comfort_score = 0
            if task_comfort == "hate_it":
                comfort_score = 0
            elif task_comfort == "dont_like_it":
                comfort_score = 0.25
            elif task_comfort == "neutral":
                comfort_score = 0.5
            elif task_comfort == "like_it":
                comfort_score = 0.75
            elif task_comfort == "love_it":
                comfort_score = 1
            else:
                return "error with calculating comfort_score for " + person
            #print("LIST OF NUMERICAL SCORES:", person, task[0], "Importance:", importance_score, "Competence:", competence_score, "Comfort:", comfort_score)
            task_score = float((importance_score + competence_score + comfort_score)/(3))  # Divide by number of metrics (1. importance, 2. competence, 3. comfort)
            score += task_score
            
        scores[person] = str(round(score, 2))
        
    
    ranked_persons = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # Create ranked_tasks list
    ranked_tasks = None
    

                
    
    return render_template("analytics.html", mode=mode, ranked_persons=ranked_persons, ranked_tasks=ranked_tasks)

    

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
        message = None
        name_already_exists_message = '<h2>Sorry, that name already exists.</h2><a href="/survey"><button class="btn btn-primary">Try again</button></a>'
        # Your code to process the form data goes here
        # Check if the data already exists in the JSON file
        try:
            with open('data/responses.json') as f:
                data = json.load(f)
                for response in data:
                    if response[0] == name:
                        message = name_already_exists_message
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

        success_message = "<h1>Thank you!</h1><p><b>Your form has been successfully submitted!</b></p><div>" + str(chore_data) + '</div><div><a href="/survey"><button class="btn btn-primary">New survey entry</button></a> <a href="/analytics"><button class="btn btn-primary">View analytics</button></a></div>'

        if message == None:
            message = success_message
        return render_template('confirmation.html', mode=mode, message=message) # 'Thanks for submitting your survey!'

        
    # Stuff for DEBUGGING
    names             = ['Aaliyah', 'Abigail', 'Adalena', 'Adalene', 'Adaleta', 'Adalicia', 'Adalina', 'Adaline', 'Adalisse', 'Adalita', 'Adaliz', 'Adalyn', 'Adalynn', 'Ahmed', 'Aiden', 'Alex', 'Alexander', 'Ali', 'Amara', 'Amelia', 'Andrés', 'Angel', 'Annabelle', 'Anthony', 'Aria', 'Arianna', 'Aubrey', 'Audrey', 'Aurora', 'Ava', 'Avery', 'Ayn', 'Baphomet', 'Bella', 'Benjamin', 'Brooklyn', 'Caleb', 'Camila', 'Carlos', 'Carter', 'Charlotte', 'Chloe', 'Daniel', 'David', 'Diego', 'Edward', 'Eleanor', 'Eli', 'Elijah', 'Elizabeth', 'Ella', 'Emily', 'Emma', 'Enrique', 'Ethan', 'Eva', 'Evelyn', 'Everly', 'Fatima', 'Francisco', 'Gael', 'Genesis', 'Grace', 'Grayson', 'Gustavo', 'Hannah', 'Harper', 'Hazel', 'Hector', 'Henry', 'Isaac', 'Isabella', 'Ivan', 'Jack', 'Jackson', 'Jacob', 'Jaime', 'James', 'Javier', 'Jaxon', 'Jayden', 'Jefferson', 'John', 'Jordan', 'Jordanne', 'Jorden', 'Jorge', 'Joseph', 'José', 'Juan', 'Julian', 'Kaylee', 'Khloé', 'Kim', 'Landon', 'Leah', 'Lee', 'Levi', 'Leviathan', 'Lex', 'Liam', 'Lilith', 'Lily', 'Lincoln', 'Logan', 'Lucas', 'Lucifer', 'Luis', 'Luke', 'Luna', 'Léo', 'Madison', 'Makayla', 'Manuel', 'Mason', 'Matthew', 'Mauricio', 'Maya', 'Mia', 'Michael', 'Miguel', 'Mila', 'Miles', 'Muhammad', 'Natalie', 'Noah', 'Nora', 'Oliver', 'Olivia', 'Oscar', 'Owen', 'Penelope', 'Rafael', 'Ricardo', 'Riley', 'Roberto', 'Ruby', 'Samael', 'Samuel', 'Satan', 'Scarlett', 'Sebastian', 'Sofia', 'Sophia', 'Stella', 'Taylor', 'Thomas', 'Victoria', 'Violet', 'Vít', 'Willow', 'Wyatt', 'Yasmin', 'Zoe']
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
    unittest.main()
