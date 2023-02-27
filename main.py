from flask import Flask, render_template, request
from datetime import datetime
import pytz
import random
import json
from collections import defaultdict
import operator


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


###########################################################################
# _______ _       _______ _           ________________________  _______   #
# (  ___  | (    /(  ___  | \  |\     /\__   __|__   __(  ____ \(  ____ \ #
# | (   ) |  \  ( | (   ) | (  ( \   / )  ) (     ) (  | (    \/| (    \/ #
# | (___) |   \ | | (___) | |   \ (_) /   | |     | |  | |      | (_____  #
# |  ___  | (\ \) |  ___  | |    \   /    | |     | |  | |      (_____  ) #
# | (   ) | | \   | (   ) | |     ) (     | |     | |  | |            ) | #
# | )   ( | )  \  | )   ( | (____/\ |     | |  ___) (__| (____/\/\____) | #
# |/     \|/    )_)/     \(_______|_/     )_(  \_______(_______/\_______) #
###########################################################################
                                                                  

@app.route("/analytics")
def analytics():
    mode = get_mode()

    with open('data/responses.json') as f:
        responses = json.load(f)
    
    # Use defaultdict to simplify the process of populating scores dictionary
    scores = defaultdict(float)
    for response in responses:
        person = response[0]
        for task in response[1:]:
            task_importance = task[1]["importance"]
            task_competence = task[1]["competence"]
            task_comfort = task[1]["comfort"]
            
            # Calculate importance, competence, and comfort scores using a dictionary
            importance_scores = {"not_important": 0, "somewhat_important": 1/3, "important": 2/3, "very_important": 1}
            competence_scores = {"cant_do_it": 0, "need_help": 0.5, "can_do_it_easily": 1}
            comfort_scores = {"hate_it": 0, "dont_like_it": 0.25, "neutral": 0.5, "like_it": 0.75, "love_it": 1}
            task_score = (importance_scores[task_importance] + competence_scores[task_competence] + comfort_scores[task_comfort]) / 3
            scores[person] += task_score
            
    # Sort scores in descending order
    ranked_persons = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
    
    # Create ranked_tasks list
    # Initialize an empty dictionary to store task scores
    task_scores = defaultdict(float)
    for task in chores:
        # Calculate the average score across all responses for this task
        task_score = sum(response[1][task]["importance"] + response[1][task]["competence"] + response[1][task]["comfort"] for response in responses) / (3 * len(responses))
        task_scores[task] = task_score
    
    # Sort task scores in descending order
    ranked_tasks = sorted(task_scores.items(), key=operator.itemgetter(1), reverse=True)
    print(ranked_tasks)

    return render_template("analytics.html", mode=mode, ranked_persons=ranked_persons, ranked_tasks=ranked_tasks)

###########################################################################
##################### END OF ANALYTICS ####################################
###########################################################################

    

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

