from dataclasses import dataclass
from models.AnswerModel import Answer
from models.UserModel import User
from models.QuestionModel import Question


@dataclass
class UserErrorDto:
    message: str = None
    body: User = None
    error: str = None


@dataclass
class QuestionErrorDto:
    message: str = None
    body: Question = None
    error: str = None


@dataclass
class AnswerErrorDto:
    message: str = None
    body: Answer = None
    error: str = None
