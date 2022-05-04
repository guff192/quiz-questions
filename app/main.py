from datetime import datetime

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select

from models import Base, Question
from database import session_local, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_session():
    session = session_local()
    try:
        yield session
    finally:
        session.close()


# Pydantic Schema
# Used as a serializer to output data from the api request
class QuestionResponse(BaseModel):
    id: int
    question_text: str
    answer_text: str
    created_at: datetime

    class Config:
        orm_mode = True


@app.get("/test/", response_model=QuestionResponse)
def get_question(db: Session = Depends(get_session)):
    # Assuming that we have some question in db
    # q = Question(question_text="what?", answer_text="42", created_at=datetime.now())
    # db.add(q)
    # db.commit()

    return db.scalars(select(Question)).first()

