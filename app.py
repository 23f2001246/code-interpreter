from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from io import StringIO
import sys
import traceback
import re

app = FastAPI(
    title="Code Interpreter API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str

class CodeResponse(BaseModel):
    error: List[int]
    result: str

def execute_python_code(code: str):
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        exec(code)
        output = sys.stdout.getvalue()
        return {"success": True, "output": output}

    except Exception:
        output = traceback.format_exc()
        return {"success": False, "output": output}

    finally:
        sys.stdout = old_stdout

@app.get("/")
def root():
    return {"message": "Code Interpreter API Running"}

@app.post("/code-interpreter", response_model=CodeResponse)
async def code_interpreter(request: CodeRequest):
    result = execute_python_code(request.code)

    if result["success"]:
        return CodeResponse(
            error=[],
            result=result["output"]
        )

    traceback_text = result["output"]

    matches = re.findall(r'line (\d+)', traceback_text)

    error_lines = []
    if matches:
        error_lines = [int(matches[-1])]

    return CodeResponse(
        error=error_lines,
        result=traceback_text
    )
