from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory storage for users
users_db = {}

# User model
class User(BaseModel):
    username: str
    password: str

# Request model for the new endpoint
class IssueRequest(BaseModel):
    issue: str
    location: str
    phone: int

# Response model for the new endpoint
class IssueResponse(BaseModel):
    complaintid: int
    esttime: str
    name: str
    phone: int

@app.post("/signup")
def sign_up(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    users_db[user.username] = user.password
    return {"code": "success"}

@app.post("/signin")
def sign_in(user: User):
    if user.username not in users_db or users_db[user.username] != user.password:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"code": "success"}

@app.post("/report_issue", response_model=IssueResponse)
def report_issue(issue_request: IssueRequest):
    # Dummy response data
    response_data = IssueResponse(
        complaintid=3210,
        esttime="2 hours",
        name="John Doe",
        phone=issue_request.phone
    )
    return response_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)