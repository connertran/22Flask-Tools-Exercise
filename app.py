from flask import Flask, request, render_template, redirect, flash
from flask import session
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = "chicken123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
debug = DebugToolbarExtension(app)

res_in_cookies = 'responses'

@app.route('/')
def show_homepage():
  """Showing the homepage"""
  return render_template('homepage.html', survey_title = surveys.satisfaction_survey.title, survey_instructions = surveys.satisfaction_survey.instructions)

@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session[res_in_cookies] = []
    print("*********restart**********")
    print(session[res_in_cookies])
    print("*********restart**********")

    return redirect("/questions/0")

@app.route('/answer',methods=["POST"])
def append_ans_to_res():
  """Saving the answers to the database"""
  choice = request.form['answer']

  responses = session[res_in_cookies]
  responses.append(choice)
  session[res_in_cookies]= responses
  print("*********res_in_cookies updated**********")
  print(session[res_in_cookies])
  print("*********res_in_cookies updated**********")

  if len(responses)== len(surveys.satisfaction_survey.questions):
    return redirect('/thank-you')
  else:
    return redirect(f"/questions/{len(responses)}")

@app.route('/thank-you')
def thank_the_user():
  """The user has completed the survey"""
  return render_template('complete.html')


@app.route('/questions/<int:num>')
def show_user_the_question(num):
    """Show the user the right answer"""
    responses = session.get(res_in_cookies)
    answers_in_responses = len(responses)
    if num <= answers_in_responses and len(surveys.satisfaction_survey.questions) != answers_in_responses:
        return render_template(
            'question.html',
            question_num=num,
            question=surveys.satisfaction_survey.questions[num].question,
            choices=surveys.satisfaction_survey.questions[num].choices
        )
    elif len(surveys.satisfaction_survey.questions) == answers_in_responses:
        # They've answered all the questions! Thank them.
        return redirect("/thank-you")
    else:
        flash(f"You're trying to access an invalid question {num}")
        return redirect(f"/questions/{answers_in_responses}")