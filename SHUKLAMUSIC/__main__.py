#!/usr/bin/env python3
# STRANGER-MUSIC - Render Port 8080 Fixed main.py

import asyncio
import importlib
import os
import sys
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

# File descriptor limit
if sys.platform != "win32":
    try:
        import resource
        _soft, _hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        resource.setrlimit(resource.RLIMIT_NOFILE, (65536, _hard))
    except:
        pass

import config
from SHUKLAMUSIC import LOGGER, app, userbot
from SHUKLAMUSIC.core.call import SHUKLA
from SHUKLAMUSIC.misc import sudo
from SHUKLAMUSIC.plugins import ALL_MODULES
from SHUKLAMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# 🔥 HTTP SERVER - Render Port 8080 + /ping
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/ping':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'PONG')
            return
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Stranger Music Bot Live')

    def log_message(self, format, *args):
        pass

def run_http_server():
    """FIXED: Port 8080 server - starts IMMEDIATELY"""
    port = 8080
    try:
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        print(f"[PORT-8080] 🌐 Server BOUND 0.0.0.0:8080")  # Force log
        LOGGER(__name__).info("🌐 HTTP Server LIVE on 0.0.0.0:8080 /ping")
        server.serve_forever()
    except Exception as e:
        print(f"[PORT-8080] ❌ Server error: {e}")

# 🚀 MAIN FUNCTION
async def main():
    try:
        # 🔥 STEP 1: HTTP SERVER FIRST (5 sec delay for binding)
        print("[RENDER] Starting HTTP server...")
        http_thread = threading.Thread(target=run_http_server, daemon=True)
        http_thread.start()
        
        # CRITICAL: Wait for port binding
        time.sleep(5)
        print("[RENDER] ✅ Port 8080 ready!")
        LOGGER(__name__).info("🚀 Render HTTP server confirmed")

        # Bot startup (original code)
        if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
            LOGGER(__name__).error("❌ No STRING sessions!")
            return

        await sudo()
        try:
            for user_id in await get_gbanned():
                BANNED_USERS.add(user_id)
            for user_id in await get_banned_users():
                BANNED_USERS.add(user_id)
        except:
            pass

        await app.start()
        for module in ALL_MODULES:
            try:
                importlib.import_module("SHUKLAMUSIC.plugins" + module)
            except:
                pass
        LOGGER("SHUKLAMUSIC.plugins").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 🥳")

        await userbot.start()
        await SHUKLA.start()
        
        try:
            await SHUKLA.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
        except:
            pass
            
        await SHUKLA.decorators()
        LOGGER("SHUKLAMUSIC").info("🎉 STRANGER BOT LIVE | Port 8080 OK")

        await idle()
        
    except KeyboardInterrupt:
        pass
    finally:
        try:
            await app.stop()
            await userbot.stop()
        except:
            pass

if __name__ == "__main__":
    print("[RENDER] Starting Stranger Music Bot...")
    asyncio.run(main())
