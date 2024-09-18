from flask import Flask
from api.user_api import fetch_users
from api.questions_api import fetch_questions_from_api
from controllers.answer_controller import answer_blueprint
from controllers.user_controller import user_blueprint
from controllers.question_controller import question_blueprint
from repository.user_repository import create_users_table
from repository.question_repository import create_questions_table, insert_questions
from repository.answer_repository import create_answers_table


app = Flask(__name__)

# users = fetch_users()
# questions = fetch_questions_from_api()
# create_users_table()
# create_questions_table()
# insert_users(users)
# insert_questions(questions)
# create_answers_table()
# answers = fetch_answers_from_api(questions)



if __name__ == "__main__":
    app.register_blueprint(user_blueprint, url_prefix="/api/users")
    app.register_blueprint(question_blueprint, url_prefix="/api/questions")
    app.register_blueprint(answer_blueprint, url_prefix="/api/answers")
    app.run(debug=True)





