from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from io import StringIO
import sys
import traceback
import re

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# Root Endpoint
# ----------------------------
@app.get("/")
async def root():
    return {"message": "API is running"}


# ----------------------------
# Code Interpreter
# ----------------------------
class CodeRequest(BaseModel):
    code: str


def execute_python_code(code: str):
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        exec(code)
        output = sys.stdout.getvalue()

        return {
            "success": True,
            "output": output
        }

    except Exception:
        output = traceback.format_exc()

        return {
            "success": False,
            "output": output
        }

    finally:
        sys.stdout = old_stdout


@app.post("/code-interpreter")
async def code_interpreter(request: CodeRequest):

    result = execute_python_code(request.code)

    if result["success"]:
        return {
            "error": [],
            "result": result["output"]
        }

    traceback_text = result["output"]

    matches = re.findall(r'line (\d+)', traceback_text)

    error_lines = []

    if matches:
        error_lines = [int(matches[-1])]

    return {
        "error": error_lines,
        "result": traceback_text
    }


# ----------------------------
# Sentiment Analysis
# ----------------------------
class SentimentRequest(BaseModel):
    sentences: List[str]


@app.post("/sentiment")
async def sentiment(request: SentimentRequest):

    positive_words = {
        "love",
        "great",
        "good",
        "excellent",
        "awesome",
        "amazing",
        "happy",
        "fantastic",
        "wonderful",
        "best",
        "nice",
        "perfect",
        "liked",
        "enjoy",
        "enjoyed"
    }

    negative_words = {
        "hate",
        "bad",
        "terrible",
        "awful",
        "sad",
        "worst",
        "horrible",
        "angry",
        "poor",
        "disappointed",
        "disappointing",
        "boring",
        "annoying",
        "useless"
    }

    results = []

    for sentence in request.sentences:

        text = sentence.lower()

        positive_score = sum(
            word in text for word in positive_words
        )

        negative_score = sum(
            word in text for word in negative_words
        )

        if positive_score > negative_score:
            sentiment = "happy"

        elif negative_score > positive_score:
            sentiment = "sad"

        else:
            sentiment = "neutral"

        results.append({
            "sentence": sentence,
            "sentiment": sentiment
        })

    return {"results": results}
