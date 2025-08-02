from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    # This block runs only when you execute `python main.py`
    uvicorn.run(
        "main:app",          # module:app
        host="0.0.0.0",      # make it reachable on your network
        port=8000,           # default FastAPI port
        reload=True          # enables hot-reload for dev (optional)
    )
