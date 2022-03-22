import copy
import random
import os

from flask import Flask, render_template, request, flash
from flask import Markup

import KeyBoardControl
import Load_Questions

app = Flask(__name__, template_folder='templates')
app.secret_key = "abc"


def shuffle(q):
    selected_keys = []
    i = 0
    while i < len(q):
        current_selection = random.choice(list(q.keys()))
        if current_selection not in selected_keys:
            selected_keys.append(current_selection)
            i = i + 1
    return selected_keys


@app.route("/")
def home():
    return render_template('home_page.html')


@app.route("/hill_climbing")
def hill_climbing():
    os.system("Hill Climb Racing")
    return render_template('home_page.html')


@app.route('/quiz_home')
def quiz_home():
    return render_template('quiz_home.html')


@app.route('/quiz_instructions')
def quiz_instructions():
    global count, correct, coin, mode

    count = 0
    correct = 0
    coin = []
    mode = ""

    return render_template('quiz_instructions.html')


@app.route('/load_all_questions', methods=['POST'])
def load_all_questions():
    global count, original_questions, questions, questions_shuffled, mode, coin

    try:

        mode = request.form["mode"]

        coin = []

        print(mode)

        original_questions = Load_Questions.load(mode)

        questions = copy.deepcopy(original_questions)

        questions_shuffled = shuffle(questions)

        print(count, questions_shuffled[count])
        print(questions[questions_shuffled[count]])
        random.shuffle(questions[questions_shuffled[count]])
        print(questions[questions_shuffled[count]])

        return render_template('quiz_questions.html', qes=questions_shuffled[count],
                               opt=questions[questions_shuffled[count]], amount=coin, choosen_opt='')
    except Exception as e:
        print(e)
        flash("Please Select Any One Mode!!")
        return render_template('quiz_instructions.html')


@app.route('/quiz_questions')
def quiz_questions():
    global count, original_questions, questions, questions_shuffled, mode, coin

    coin = []

    print(count, questions_shuffled[count])
    print(questions[questions_shuffled[count]])
    random.shuffle(questions[questions_shuffled[count]])
    print(questions[questions_shuffled[count]])

    return render_template('quiz_questions.html', qes=questions_shuffled[count],
                           opt=questions[questions_shuffled[count]], amount=coin, choosen_opt='', )


@app.route('/check_answer', methods=['POST'])
def check_answer():
    global count, correct, original_questions, questions, questions_shuffled, mode, coin ,cap

    try:
        print(count, questions_shuffled[count])

        if mode == 'easy':
            coin = ["static/coin.png"]
        elif mode == 'medium':
            coin = ["static/coin.png"] * 3
        elif mode == 'hard':
            coin = ["static/coin.png"] * 5

        print(coin)

        print(original_questions[questions_shuffled[count]][0])

        answered = KeyBoardControl.get_option(cap)
        answered = questions[questions_shuffled[count]][answered - 1]

        # answered = request.form[questions_shuffled[count]]

        if original_questions[questions_shuffled[count]][0] == answered:
            correct+=1
            return render_template('quiz_questions.html', qes=questions_shuffled[count],
                                   opt=questions[questions_shuffled[count]], amount=coin,
                                   choosen_opt=answered,
                                   crt_opt=original_questions[questions_shuffled[count]][0],
                                   crt_answer=Markup('You Are Correct!!<br>Correct Answer : {}'.format(answered)))
        else:
            return render_template('quiz_questions.html', qes=questions_shuffled[count],
                                   opt=questions[questions_shuffled[count]], amount=[],
                                   choosen_opt=answered,
                                   crt_opt=original_questions[questions_shuffled[count]][0],
                                   crt_answer=Markup('You Are Wrong!!<br>Correct Answer : {}'.format(
                                       original_questions[questions_shuffled[count]][0])))

    except Exception as e:
        coin = []
        print(e)
        flash("Please Select Any One Option!!")
        return render_template('quiz_questions.html', qes=questions_shuffled[count],
                               choosen_opt='',
                               opt=questions[questions_shuffled[count]], amount=coin, crt_answer='')


@app.route('/next_question')
def next_question():
    global count, correct, original_questions, questions, questions_shuffled, mode, coin, cap

    try:

        next_ques = KeyBoardControl.get_next_question(cap)

        if next_ques == 0:
            count += 1
            if count == 5:
                return quiz_results()
            return quiz_questions()

        else:
            x = 1/0

    except Exception:
        coin = []
        flash("Do Something!!")
        return render_template('quiz_questions.html', qes=questions_shuffled[count],
                               opt=questions[questions_shuffled[count]], amount=coin, choosen_opt='', )


@app.route('/quiz_results')
def quiz_results():
    return render_template('quiz_results.html', res=correct)


if __name__ == '__main__':

    cap = KeyBoardControl.open_camera()

    original_questions = {}

    # print(original_questions)

    questions = {}

    coin = []

    questions_shuffled = {}

    mode = ""

    count = 0
    correct = 0

    app.run(debug=True)
