from flask import Flask, session, render_template, redirect, url_for, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.debug = True
app.secret_key = 'supersecretkey'
toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route('/')
def start():
    return render_template('start.html', survey=satisfaction_survey)

@app.route('/start_survey', methods=['POST'])
def start_survey():
    session['responses'] = []
    return redirect(url_for('question', qid=0))

@app.route('/questions/<int:qid>')
def question(qid):
    # Check if the user is attempting to access a question in order
    if 'responses' not in session:
        return redirect(url_for('start'))

    responses = session.get('responses', [])
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
    # Update the responses list in the session
    answer = request.form.get('answer')
    qid = int(request.form.get('qid'))

    if 'responses' not in session:
        return redirect(url_for('start'))

    responses = session.get('responses', [])
    
    if answer:
        responses.append(answer)
        session['responses'] = responses

    next_qid = qid + 1
    if next_qid >= len(satisfaction_survey.questions):
        return redirect(url_for('thank_you'))
    else:
        return redirect(url_for('question', qid=next_qid))

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == "__main__":
    app.run()
