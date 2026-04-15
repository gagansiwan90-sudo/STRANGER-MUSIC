# ===== YOUR EXISTING BOT CODE (same रखो) =====

# ===== PORT 8000 के लिए यह add करो =====
from fastapi import FastAPI
import uvicorn
import threading
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "AdamMusic_Bot Live! 🎵", "port": 8000}

@app.get("/health")
def health():
    return {"status": "healthy", "bot": "running"}

def http_server():
    port = 8000  # Fixed port 8000
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

# Bot start होने के बाद HTTP server start
if __name__ == "__main__":
    # Your bot code runs first...
    
    # फिर background में HTTP server
    server_thread = threading.Thread(target=http_server, daemon=True)
    server_thread.start()
    
    # Bot को running रखो
    import time
    while True:
        time.sleep(1)
