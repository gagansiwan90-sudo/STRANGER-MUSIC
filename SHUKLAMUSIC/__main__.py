# Add to your main.py or app.py (at the end)
import uvicorn
from fastapi import FastAPI
import threading
import os

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "healthy", "bot": "AdamMusic_Bot"}

@app.get("/")
async def root():
    return {"message": "AdamMusic_Bot is running! 🎵"}

def run_web_server():
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

# Start web server in background thread
if __name__ == "__main__":
    # Your existing bot code here...
    
    # Start HTTP server in background
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()u
