import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

class Email(BaseModel):
    email: str

class EmailList(BaseModel):
    emailList: list[Email]

app = FastAPI(debug=True)

origins = [
    "http://localhost:3000",
    # Add more origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_db = {"emails":[]} 

@app.get("/emails", response_model=EmailList)
def get_emails():
    return EmailList(emailList=memory_db["emails"])

@app.post("/emails")
def add_email(email: Email):
    memory_db["emails"].append(email)
    return email
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)