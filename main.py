import logging
import uuid
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, users, issues, service_engineers
from sqlalchemy import select, update

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
    email: str
    password: str

class Admin(BaseModel):
    username: str
    password: str

# Request model for the new endpoint
class IssueRequest(BaseModel):
    issue: str
    location: str
    phone: int
    user_id: str

# Response model for the new endpoint
class IssueResponse(BaseModel):
    complaintid: str
    esttime: str
    name: str
    phone: int

# Service Engineer model
class ServiceEngineer(BaseModel):
    name: str
    availability: bool

@app.post("/signup")
def sign_up(user: User, db: Session = Depends(get_db)):
    user_id = str(uuid.uuid4())
    stmt = select(users).where(users.c.username == user.username)
    existing_user = db.execute(stmt).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    db.execute(users.insert().values(user_id=user_id, username=user.username, email=user.email, password=user.password))
    db.commit()
    return {"code": "success", "user_id": user_id}

@app.post("/signin")
def sign_in(user: User, db: Session = Depends(get_db)):
    stmt = select(users).where(users.c.username == user.username, users.c.password == user.password)
    existing_user = db.execute(stmt).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"code": "success"}

@app.post("/report_issue", response_model=IssueResponse)
def report_issue(issue_request: IssueRequest, db: Session = Depends(get_db)):
    # Check if user exists
    stmt = select(users).where(users.c.user_id == issue_request.user_id)
    existing_user = db.execute(stmt).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid user_id")

    # Find an available service engineer
    stmt = select(service_engineers).where(service_engineers.c.availability == True)
    available_engineer = db.execute(stmt).first()
    if not available_engineer:
        raise HTTPException(status_code=400, detail="No available service engineers")

    # Generate unique complaint ID
    complaintid = str(uuid.uuid4())

    # Dummy response data
    response_data = IssueResponse(
        complaintid=complaintid,
        esttime="2 hours",
        name=available_engineer.name,
        phone=issue_request.phone
    )

    # Insert issue into the database
    db.execute(issues.insert().values(
        issue=issue_request.issue,
        location=issue_request.location,
        phone=issue_request.phone,
        complaintid=response_data.complaintid,
        esttime=response_data.esttime,
        name=response_data.name,
        user_id=issue_request.user_id,
        status="open"
    ))

    # Update engineer availability to offline
    db.execute(update(service_engineers).where(service_engineers.c.id == available_engineer.id).values(availability=False))

    db.commit()
    return response_data

@app.post("/admin_signin")
def admin_signin(user: Admin, db: Session = Depends(get_db)):
    # Dummy admin credentials
    admin_username = "admin"
    admin_password = "adminpass"
    if user.username != admin_username or user.password != admin_password:
        raise HTTPException(status_code=400, detail="Invalid admin credentials")
    return {"code": "success"}

@app.post("/add_engineer")
def add_engineer(engineer: ServiceEngineer, db: Session = Depends(get_db)):
    db.execute(service_engineers.insert().values(name=engineer.name, availability=engineer.availability))
    db.commit()
    return {"code": "success"}

if __name__ == "__main__":
    import uvicorn
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")