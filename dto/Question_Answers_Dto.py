from dataclasses import dataclass


@dataclass
class Question_Answer:
    question_text: str
    correct_answer: str
    incorrect_answers: list
