# -----------------------------------------------
# 🔸 StrangerMusic Project
# 🔹 Developed & Maintained by: Shashank Shukla (https://github.com/itzshukla)
# 📅 Copyright © 2022 – All Rights Reserved
#
# 📖 License:
# This source code is open for educational and non-commercial use ONLY.
# You are required to retain this credit in all copies or substantial portions of this file.
# Commercial use, redistribution, or removal of this notice is strictly prohibited
# without prior written permission from the author.
#
# ❤️ Made with dedication and love by ItzShukla
# -----------------------------------------------
 import asyncio
import importlib
import os
import sys
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

# File descriptor limit for Linux
if sys.platform != "win32":
    try:
        import resource
        _soft, _hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        _target = min(65536, _hard)
        if _soft < _target:
            resource.setrlimit(resource.RLIMIT_NOFILE, (_target, _hard))
    except Exception:
        pass

import config
from SHUKLAMUSIC import LOGGER, app, userbot
from SHUKLAMUSIC.core.call import SHUKLA
from SHUKLAMUSIC.misc import sudo
from SHUKLAMUSIC.plugins import ALL_MODULES
from SHUKLAMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# HTTP Server for Render (Port 8080 + /ping)
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
        self.wfile.write(b'Stranger Music Bot Live ✅')
    
    def log_message(self, format, *args):
        pass

def run_http_server():
    """HTTP server on FIXED port 8080 for Render"""
    port = 8080  # FIXED - matches your Render setting
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    LOGGER(__name__).info("🌐 HTTP Health server BOUND on 0.0.0.0:8080 (/ping)")
    server.serve_forever()

async def main():
    try:
        # 🚀 STEP 1: HTTP SERVER FIRST (CRITICAL for Render)
        LOGGER(__name__).info("🚀 Starting HTTP server for Render...")
        http_thread = threading.Thread(target=run_http_server, daemon=True)
        http_thread.start()
        time.sleep(3)  # Wait for port binding
        LOGGER(__name__).info("✅ Port 8080 ready for Render health check")

        # Step 2: Validate sessions
        if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
            LOGGER(__name__).error("❌ No assistant sessions found!")
            return

        # Step 3: Load banned users
        try:
            users = await get_gbanned()
            for user_id in users:
                BANNED_USERS.add(user_id)
            users = await get_banned_users()
            for user_id in users:
                BANNED_USERS.add(user_id)
        except:
            pass

        # Step 4: Sudo setup
        await sudo()
        LOGGER("SHUKLAMUSIC").info("👑 SUDO users loaded")

        # Step 5: Start main bot
        await app.start()
        LOGGER("SHUKLAMUSIC.core.bot").info("🤖 Main bot started")

        # Step 6: Load plugins
        for module in ALL_MODULES:
            try:
                importlib.import_module("SHUKLAMUSIC.plugins" + module)
            except Exception as e:
                LOGGER("SHUKLAMUSIC.plugins").error(f"Plugin {module} failed: {e}")
        LOGGER("SHUKLAMUSIC.plugins").info("🔌 All Features Loaded Baby🥳...")

        # Step 7: Start userbot & VC
        await userbot.start()
        await SHUKLA.start()
        LOGGER("SHUKLAMUSIC.core.userbot").info("🎤 Assistants & VC started")

        # Step 8: VC test
        try:
            await SHUKLA.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
            LOGGER("SHUKLAMUSIC").info("✅ VC test passed")
        except NoActiveGroupCall:
            LOGGER("SHUKLAMUSIC").warning("⚠️ Start VC in log group")
        except:
            pass

        await SHUKLA.decorators()

        # 🎉 BOT READY
        LOGGER("SHUKLAMUSIC").info(
            "🎉 STRANGER MUSIC BOT FULLY STARTED!
"
            "🌐 HTTP Health: http://your-domain:8080/ping
"
            "📱 Test Commands: /start /help
"
            "╔═════ஜ۩۞۩ஜ════╗
"
            "  ☠︎︎𝗠𝗔𝗗𝗘 𝗕𝗬 𝗠𝗥 𝗦𝗛𝗜𝗩𝗔𝗡𝗦𝗛
"
            "╚═════ஜ۩۞۩ஜ════╝"
        )

        # Keep running
        await idle()

    except KeyboardInterrupt:
        LOGGER("SHUKLAMUSIC").info("🛑 Bot stopped by user")
    except Exception as e:
        LOGGER("SHUKLAMUSIC").error(f"❌ Critical error: {e}", exc_info=True)
    finally:
        try:
            await app.stop()
            await userbot.stop()
            LOGGER("SHUKLAMUSIC").info("🔄 Cleanup complete")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(main())
