from fastapi import FastAPI, Depends # type: ignore
from database import engine, SessionLocal
from models import Base
from models import User
from models import Post
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from schemas import UserCreate, UserLogin, PostCreate
from jose import jwt, JWTError

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/health")
def health_post():
    return {"status": "posted"}

@app.get("/hello")
def hello():
    return {"message": "You die, I die"}

# adding a user to a database
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# Auth dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str= Depends(oauth2_scheme), db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except(JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# creating users / user registration
@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, password_hash=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id":new_user.id, "username":new_user.username}

# getting user by ID
@app.get ("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "username": user.username}


# login endpoint creation
@app.post ("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}


# POST posting
@app.post("/posts")
def create_post(post: PostCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    db_post = Post(title=post.title, content=post.content, owner_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return {"id": db_post.id, "title": db_post.title, "content": db_post.content, "owner_id": current_user.id}

# PUT posts / AuthZ / Update
@app.put ("/posts/{post_id}")
def get_post(post_id: int, title: str, content: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException (status_code=404, detail="Post not found")

    # AuthZ check
    if post.owner_id != current_user.id:
        raise HTTPException (status_code=403, detail="Not authorized to edit this post")
    
    post.title = title
    post.content = content
    db.commit()
    db.refresh(post)

    return {"id": post.id, "title": post.title, "content": post.content, "owner_id": post.owner_id}


# post DELETE
@app.delete ("/posts/{post_id}")
def delete_post(post_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException (status_code=404, detail="Post not found")

    # AuthZ check
    if post.owner_id != current_user.id:
        raise HTTPException (status_code=403, detail="Not authorized to delete this post")

    db.delete(post)
    db.commit()

    return {"message": "Post deleted"}
