from fastapi import FastAPI
from pydantic import BaseModel
import os
import redis
import logging

app = FastAPI()

class Question(BaseModel):
    question: str

redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = os.environ.get('REDIS_PORT', 6379)
redis_db = os.environ.get('REDIS_DB', 0)

redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

def store_question_result(question: str, result: str):
    try:
        redis_client.set(question, result)
        logging.info(f"Stored result for question {question} in Redis")
        return True
    except Exception as e:
        logging.error(f"Failed to store result for question {question} in Redis: {e}")
        return False

@app.post("/generate")
async def generate(question: Question):
    # fake the result
    result = f"This is a fake result for question {question.question}"
    store_question_result(question.question, result)
    return {"result": result}

if __name__ == "__main__":
    import uvicorn
    # init logging
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000)