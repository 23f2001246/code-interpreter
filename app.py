from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

class SentimentRequest(BaseModel):
sentences: List[str]

@app.post("/sentiment")
async def sentiment(request: SentimentRequest):

```
positive_words = {
    "love", "great", "good", "excellent", "awesome",
    "amazing", "happy", "fantastic", "wonderful", "best"
}

negative_words = {
    "bad", "terrible", "awful", "hate", "worst",
    "sad", "angry", "horrible", "poor", "disappointed"
}

results = []

for sentence in request.sentences:
    text = sentence.lower()

    pos = sum(word in text for word in positive_words)
    neg = sum(word in text for word in negative_words)

    if pos > neg:
        sentiment = "happy"
    elif neg > pos:
        sentiment = "sad"
    else:
        sentiment = "neutral"

    results.append({
        "sentence": sentence,
        "sentiment": sentiment
    })

return {"results": results}
```
