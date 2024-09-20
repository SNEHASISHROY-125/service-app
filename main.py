from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, users, issues
from sqlalchemy import select

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
def sign_up(user: User, db: Session = Depends(get_db)):
    stmt = select(users).where(users.c.username == user.username)
    existing_user = db.execute(stmt).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    db.execute(users.insert().values(username=user.username, password=user.password))
    db.commit()
    return {"code": "success"}

@app.post("/signin")
def sign_in(user: User, db: Session = Depends(get_db)):
    stmt = select(users).where(users.c.username == user.username, users.c.password == user.password)
    existing_user = db.execute(stmt).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"code": "success"}

@app.post("/report_issue", response_model=IssueResponse)
def report_issue(issue_request: IssueRequest, db: Session = Depends(get_db)):
    # Dummy response data
    response_data = IssueResponse(
        complaintid=3210,
        esttime="2 hours",
        name="John Doe",
        phone=issue_request.phone
    )
    db.execute(issues.insert().values(
        issue=issue_request.issue,
        location=issue_request.location,
        phone=issue_request.phone,
        complaintid=response_data.complaintid,
        esttime=response_data.esttime,
        name=response_data.name
    ))
    db.commit()
    return response_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)