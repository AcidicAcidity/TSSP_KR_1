from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class User(BaseModel):
    name: str
    message: int

class FeedbackValidated(BaseModel):
    name: str = Field(..., min_lenght=2, max_lenght=50, description="Имя пользователя")
    message: str = Field(..., min_lenght=10, max_lenght=500, description="Сообщение отзыва")

    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:

        forbidden_words = ['крингк', 'рофл', 'вайбик']
        message_lower = v.lower()

        for word in forbidden_words:
            pattern = r'\b' + re.escape(word) + r'\b'
            if re.search(pattern, message_lower):
                raise ValueError('Использование недопустимых слов')

        return v