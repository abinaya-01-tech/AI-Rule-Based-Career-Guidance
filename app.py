from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Home page - collect user info
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['age'] = int(request.form['age'])
        if session['age'] < 0:
            return "Invalid age"
        session['email'] = request.form['email']
        return redirect(url_for('quiz'))
    return render_template('home.html')

# Quiz page
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # Initialize scores
        logic = creativity = communication = leadership = tech = 0
        answers = ['q1','q2','q3','q4','q5','q6','q7','q8']

        for q in answers:
            ans = request.form[q].upper()
            if q in ['q1','q3','q4','q7']:
                if ans == 'A':
                    logic += 1
                elif ans == 'B':
                    creativity += 1
                elif ans == 'C':
                    communication += 1
                elif ans == 'D':
                    leadership += 1
            elif q in ['q2','q5','q6','q8']:
                if ans == 'A':
                    tech += 1
                elif ans == 'B':
                    creativity += 1
                elif ans == 'C':
                    communication += 1
                elif ans == 'D':
                    leadership += 1

        traits = {
            'Logic': logic,
            'Creativity': creativity,
            'Communication': communication,
            'Leadership': leadership,
            'Tech': tech
        }

        # Store the strongest trait in session
        session['career_trait'] = max(traits, key=traits.get)
        return redirect(url_for('results'))

    return render_template('quiz.html')

# Result page
@app.route('/results')
def results():
    name = session.get('name')
    age = session.get('age')
    email = session.get('email')

    # Map traits to specific careers
    career_mapping = {
        'Logic': "Data Scientist, Mathematician, Analyst",
        'Creativity': "Graphic Designer, Artist, Content Creator",
        'Communication': "Teacher, Public Speaker, Counselor",
        'Leadership': "Project Manager, Entrepreneur, Team Lead",
        'Tech': "Software Engineer, AI Developer, Web Developer"
    }

    strongest_trait = session.get('career_trait')
    career = career_mapping.get(strongest_trait, "Various Careers")

    return render_template('result.html', name=name, age=age, email=email, career=career)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
