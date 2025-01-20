from fastapi import FastAPI
from routes import generate, vocab

app = FastAPI()

# Include routers
app.include_router(generate.router)
app.include_router(vocab.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
