from typing import List

from models.AnswerModel import Answer


def create_answers(question_id: int, incorrect_answers: List[str]) -> List[Answer]:
    return [
        Answer(question_id=question_id, incorrect_answer=answer)
        for answer in incorrect_answers
    ]




