from datetime import datetime

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select

import models
from database import session_local, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


# Pydantic Schema
# Used as a serializer to output data from the api request
class QuestionBase(BaseModel):
    id: int
    question_text: str
    answer_text: str
    created_at: datetime

    class Config:
        orm_mode = True


@app.get("/test/", response_model=QuestionBase)
def get_question(db: Session = Depends(get_db)):
    # Assuming that we have some question in db
    # q = models.Question(id=1, question_text="what?", answer_text="42", created_at=datetime.now())
    # db.add(q)
    # db.commit()

    return db.scalars(select(models.Question)).first()
