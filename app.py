from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def start_survey_page():
    """Show survey homepage"""
    return render_template("start_survey.html", survey=survey)

@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses"""
    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route('/answer', methods=["POST"])
def next_question():
    """Save response and continue to next question"""
    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if(len(responses) == len(survey.questions)):
        return redirect("/complete")
    
    else:
        return redirect(f'/question/{len(responses)}')
    
@app.route("/questions/<int:qid>")
def show_question(qid):
    """Go to current question"""
    responses = session.get(RESPONSES_KEY)
    if (responses is None):
        return redirect("/")
    
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qid]
    return render_template("questions.html", question_num=qid, question=question)


@app.route("/complete")
def complete_survey():
    """Show thank you page at end of survey"""
    return render_template("completion.html")