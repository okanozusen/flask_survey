from flask import Flask, render_template, redirect, url_for,request,flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.debug = True
app.secret_key = 'supersecretkey'  
toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

responses = []

@app.route('/')
def start():
    return render_template('start.html', survey=satisfaction_survey)

@app.route('/questions/<int:qid>')
def question(qid):
    if qid < len(satisfaction_survey.questions):
        if len(responses) == qid:
            return render_template('question.html', question=satisfaction_survey.questions[qid], qid=qid)
        else:
            flash('You are trying to access a question out of order.', 'warning')
            return redirect(url_for('question', qid=len(responses)))
    else:
        return redirect(url_for('thank_you'))
   
@app.route('/answer', methods=['POST'])
def answer():
    global responses
    answer = request.form.get('answer')
    qid = int(request.form.get('qid'))
    
    if answer:
        responses.append(answer)
    
    next_qid = qid + 1
    if next_qid >= len(satisfaction_survey.questions):
        return redirect(url_for('thank_you'))
    else:
        return redirect(url_for('question', qid=next_qid))


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')
