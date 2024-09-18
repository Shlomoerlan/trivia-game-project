from models.QuestionModel import Question
import requests
from typing import List


def process_question(q) -> Question:
    return Question(
        question_text=q["question"],
        correct_answer=q["correct_answer"]
    )


def fetch_questions_from_api() -> List[Question]:
    response = requests.get("https://opentdb.com/api.php?amount=20")

    return list(
        map(process_question, response.json()["results"])
    ) if response.status_code == 200 else []


print(fetch_questions_from_api())