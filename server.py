from flask import Flask, render_template, request, redirect, url_for
import connection
import util

app = Flask(__name__)
PATH = app.root_path

ID = 0
TIME = 1
TITLE = 2
CONTENT = -2


@app.route("/")
@app.route("/list")
def list():
    data = connection.get_data('question.csv', PATH)

    return render_template('list.html', data=data, TITLE=TITLE, ID=ID)


@app.route("/question/<question_id>", methods=['POST', 'GET'])
def question(question_id):
    questions = connection.get_data('question.csv', PATH)
    answers = connection.get_data('answer.csv', PATH)
    for q in questions:
        if question_id == q[0]:
            question = q
    answer= [a for a in answers if a[0] == question_id]
    return render_template('question.html', question=question, question_id=question_id, answer=answer)


@app.route("/add_question", methods=['POST', 'GET'])
def add_question():
    if request.method == 'POST':
        id = util.id_generator()
        submission_time = util.get_time()
        # view_number = request.form[]
        # vote_number = request.form[]
        title = request.form['question_title']
        message = request.form['question']
        # image = request.form[]
        questions = connection.get_data('question.csv', PATH)
        data_to_save = [id,submission_time,title,message,"image"]

        # question_to_save = questions.append(data_to_save)

        connection.save_data(PATH, 'question.csv', data_to_save, 'a')
        data = connection.get_data('question.csv', PATH)
        return render_template('list.html', data=data, TITLE=TITLE, ID=ID )

    return render_template('add_question.html')


@app.route("/question/<question_id>/new-answer", methods=['POST', 'GET'])
def add_answer(question_id):
    if request.method == 'POST':
        answers = connection.get_data('answer.csv', PATH)
        question_data = connection.get_data('question.csv', PATH)
        question = [q for q in question_data if question_data[0] == question_id]
        answer = request.form['answer']
        answer_to_save = [question_id, answer]

        answers.append(answer_to_save)
        connection.save_data(PATH, 'answer.csv', answer_to_save, 'a')

        return redirect(url_for('question', question_id=question_id ))
    else:
        answers = connection.get_data('answer.csv', PATH)
        question_data = connection.get_data('question.csv', PATH)
        question = [q for q in question_data if question_data[0] == question_id]
        answer = [a for a in answers if answers[0] == question_id]
        return render_template('add_answer.html', question=question, answer=answer, question_id=question_id, )

@app.route("/question/<question_id>/delete")
def delete():
    data = connection.get_data('question.csv', PATH)
    return render_template('list.html', data=data)


@app.route("/question/<question_id>/edit", methods=['POST', 'GET'])
def edit(question_id):
    edit = True
    if request.method == 'POST':
        id = question_id
        # view_number = request.form[]
        # vote_number = request.form[]
        title = request.form['question_title']
        message = request.form['question']
        # image = request.form[]

        questions = connection.get_data('question.csv', PATH)
        index = questions.index([q for q in questions if q[ID] == question_id][0])
        submission_time = questions[index][TIME]
        questions[index] = [id, submission_time, title, message, "image"]

        connection.save_edited_data(PATH, 'question.csv', questions,'w')

        return redirect(url_for('question', question_id=question_id ))
    else:
        questions= connection.get_data('question.csv', PATH)
        question = [q for q in questions if q[0] == question_id][0]

        return render_template('add_question.html', edit=edit, question_id=question_id, question=question, TITLE=TITLE, CONTENT=CONTENT)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5050,
        debug=True,
    )
#id,submission_time,vote_number,question_id,message,image
