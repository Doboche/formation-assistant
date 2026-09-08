from pydantic import BaseModel, Field, model_validator

class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: int
    explanation: str


    @model_validator(mode='after')
    def check_correct_answer(self):
        if self.correct_answer < 0 or self.correct_answer >= len(self.options):
            raise ValueError(f"correct_answer ({self.correct_answer}) hors limites pour {len(self.options)} options")
        return self

class Quiz(BaseModel):
    quiz: list[QuizQuestion]


class Section(BaseModel):
    title: str
    content: str

class FlashCard(BaseModel):
    sections: list[Section]  = Field(min_length=2)