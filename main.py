from fastapi import FastAPI # type: ignore

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/health")
def health_post():
    return {"status": "posted"}

@app.get("/hello")
def hello():
    return {"message": "You die, I die"}
