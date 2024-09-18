from typing import List
import requests
from dto.Question_Answers_Dto import Question_Answer


def fetch_question_answers_from_api(api_url: str) -> List[Question_Answer]:
    response = requests.get(api_url)

    if response.status_code != 200:
        return []

    data = response.json()["results"]

    question_answers = [
        Question_Answer(
            question_text=entry["question"],
            correct_answer=entry["correct_answer"],
            incorrect_answers=entry["incorrect_answers"]
        )
        for entry in data
    ]

    return question_answers


api_url = "https://opentdb.com/api.php?amount=20"
questions = fetch_question_answers_from_api(api_url)

# print(questions)