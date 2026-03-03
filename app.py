from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from pydantic import ValidationError
import uvicorn
from typing import List, Dict, Any

from models import User, UserAge, FeedBack, FeedbackValidated
from feedback_store import feedbacks

app = FastAPI(
    title="Контрольная №1",
    description="Технологии работки серверных приложений",
    version="1.0.0"
)
@app.get("/", response_class=JSONResponse)
async def root():
    return {"message": "Автоперезагрузка действительно работает"}

@app.get("/html", response_class=HTMLResponse)
async def get_html_page():
    return FileResponse("index.html")

@app.post("/calculate")
async def calculate(num1: float, num2: float):
    result = num1 + num2
    return {"result": result}

# ============================================

user_instance = User(name="Александров Егор Вадимович", id=1)

@app.get("/users", response_model=User)
async def get_user():
    return user_instance

@app.post("/user")
async def check_user_adult(user: UserAge):
    is_adult = user.age >= 18
    response = user.model_dump()
    response["is_adult"] = is_adult
    return response

@app.post("/feedback")
async def create_feedback(feedback: FeedBack):
    feedback_data = feedback.model_dump()
    feedbacks.append(feedback_data)

    print(f"Получен отзыв от {feedback.name}: {feedback.message}")
    print(f"Всего отзывов: {len(feedbacks)}")

    return {"message": f"Feedback received. Thank you, {feedback.name}."}

@app.post("/feedback/validated")
async def create_validated_feedback(feedback: FeedbackValidated):
    feedback_data = feedback.model_dump()
    feedbacks.append(feedback_data)

    return {"message": f"Спасибо, {feedback.name}! Ваш отзыв сохранен."}

@app.get("/feedbacks")
async def get_all_feedbacks():
    return {"feedbacks": feedbacks, "total": len(feedbacks)}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Сервер работает корректно"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)