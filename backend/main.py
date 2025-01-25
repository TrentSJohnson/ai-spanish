from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx

from routes import generate, vocab

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vite's default development port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    # Check MongoDB connection
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        import os
        
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://mongodb:27017")
        client = AsyncIOMotorClient(mongodb_url)
        await client.admin.command('ping')
        mongodb_status = "healthy"
    except Exception as e:
        mongodb_status = f"unhealthy: {str(e)}"

    # Check Keycloak connection
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get('http://keycloak:8080/health')
            keycloak_status = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception as e:
        keycloak_status = f"unhealthy: {str(e)}"

    status_code = status.HTTP_200_OK if all(s == "healthy" for s in [mongodb_status, keycloak_status]) else status.HTTP_503_SERVICE_UNAVAILABLE

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "healthy" if status_code == 200 else "unhealthy",
            "mongodb": mongodb_status,
            "keycloak": keycloak_status
        }
    )

# Include routers
app.include_router(generate.router)
app.include_router(vocab.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
