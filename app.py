from flask import Flask

from controllers.answer_controller import answer_blueprint
from controllers.user_controller import user_blueprint
from controllers.question_controller import question_blueprint

app = Flask(__name__)

if __name__ == "__main__":
    app.register_blueprint(user_blueprint, url_prefix="/api/users")
    app.register_blueprint(question_blueprint, url_prefix="/api/questions")
    app.register_blueprint(answer_blueprint, url_prefix="/api/answers")
    app.run(debug=True)
