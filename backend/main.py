import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select
from .database import Base, engine, get_db
from . import models, schemas
from .security import hash_password, verify_password, create_token, token_user_id
@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(bind=engine)
    yield
app = FastAPI(title="Job Application Tracker API", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=[os.getenv("FRONTEND_ORIGIN","http://localhost:5173"),"http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
bearer = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)
def current_user(token: str|None=Depends(bearer), db: Session=Depends(get_db)):
    uid = token_user_id(token) if token else None
    user = db.get(models.User, uid) if uid else None
    if not user: raise HTTPException(401, "Please sign in again.")
    return user
@app.get("/api/health")
def health(): return {"status":"ok"}
@app.post("/api/auth/register", response_model=schemas.TokenOut, status_code=201)
def register(data: schemas.RegisterIn, db: Session=Depends(get_db)):
    email=data.email.lower()
    if db.scalar(select(models.User).where(models.User.email==email)): raise HTTPException(409,"Email already registered.")
    user=models.User(name=data.name.strip(),email=email,password_hash=hash_password(data.password))
    db.add(user); db.commit(); db.refresh(user)
    return {"access_token":create_token(user.id),"user":user}
@app.post("/api/auth/login", response_model=schemas.TokenOut)
def login(data: schemas.LoginIn, db: Session=Depends(get_db)):
    user=db.scalar(select(models.User).where(models.User.email==data.email.lower()))
    if not user or not verify_password(data.password,user.password_hash): raise HTTPException(401,"Incorrect email or password.")
    return {"access_token":create_token(user.id),"user":user}
@app.get("/api/applications", response_model=list[schemas.ApplicationOut])
def list_apps(user: models.User=Depends(current_user), db: Session=Depends(get_db)):
    return list(db.scalars(select(models.Application).where(models.Application.owner_id==user.id).order_by(models.Application.id.desc())))
@app.post("/api/applications", response_model=schemas.ApplicationOut, status_code=201)
def create_app(data: schemas.ApplicationIn, user: models.User=Depends(current_user), db: Session=Depends(get_db)):
    item=models.Application(**data.model_dump(),owner_id=user.id); db.add(item); db.commit(); db.refresh(item); return item
@app.patch("/api/applications/{item_id}", response_model=schemas.ApplicationOut)
def update_app(item_id:int, data:schemas.ApplicationUpdate, user:models.User=Depends(current_user), db:Session=Depends(get_db)):
    item=db.scalar(select(models.Application).where(models.Application.id==item_id,models.Application.owner_id==user.id))
    if not item: raise HTTPException(404,"Application not found.")
    for k,v in data.model_dump(exclude_unset=True).items(): setattr(item,k,v)
    db.commit(); db.refresh(item); return item
@app.delete("/api/applications/{item_id}", status_code=204)
def delete_app(item_id:int, user:models.User=Depends(current_user), db:Session=Depends(get_db)):
    item=db.scalar(select(models.Application).where(models.Application.id==item_id,models.Application.owner_id==user.id))
    if not item: raise HTTPException(404,"Application not found.")
    db.delete(item); db.commit()
@app.get("/api/dashboard")
def dashboard(user:models.User=Depends(current_user), db:Session=Depends(get_db)):
    items=list(db.scalars(select(models.Application).where(models.Application.owner_id==user.id)))
    statuses=["Applied","Interview","Assessment","Offer","Rejected"]
    return {"total":len(items),"status_counts":{s:sum(x.status==s for x in items) for s in statuses}}
