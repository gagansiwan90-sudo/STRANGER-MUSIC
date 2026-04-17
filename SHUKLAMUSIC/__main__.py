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
from http.server import HTTPServer, BaseHTTPRequestHandler
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

# File descriptor limit (Linux)
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

# HTTP Server for Render health checks
class HealthCheckHandler(BaseHTTPRequestHandler):
    """Simple HTTP handler for Render health checks"""
    
    def do_GET(self):
        """Handle GET requests"""
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Stranger Music Bot Running')
    
    def log_message(self, format, *args):
        """Suppress log messages"""
        pass

def run_http_server():
    """Run HTTP server for Render"""
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    LOGGER(__name__).info(f"🌐 HTTP health check server started on port {port}")
    server.serve_forever()

async def main():
    try:
        # Step 1: Check string sessions
        if (
            not config.STRING1
            and not config.STRING2
            and not config.STRING3
            and not config.STRING4
            and not config.STRING5
        ):
            LOGGER(__name__).error("String Session Not Filled")
            return

        # Step 2: Start HTTP server thread (Render)
        http_thread = threading.Thread(target=run_http_server, daemon=True)
        http_thread.start()
        LOGGER(__name__).info("🌐 HTTP server thread started for Render")

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
        
        # Step 5: Start main bot
        await app.start()
        
        # Step 6: Load plugins
        for module in ALL_MODULES:
            try:
                importlib.import_module("SHUKLAMUSIC.plugins" + module)
            except Exception as e:
                LOGGER("SHUKLAMUSIC.plugins").error(f"Failed {module}: {e}")
        LOGGER("SHUKLAMUSIC.plugins").info("All Features Loaded Baby🥳...")

        # Step 7: Start userbot + VC handler
        await userbot.start()
        await SHUKLA.start()

        # Step 8: VC test
        try:
            await SHUKLA.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
        except NoActiveGroupCall:
            LOGGER("SHUKLAMUSIC").error(
                "Plz Start Log Group Voicechat
Bot Continuing..."
            )
        except:
            pass

        await SHUKLA.decorators()
        LOGGER("SHUKLAMUSIC").info(
            "🎉 Stranger Music Bot Started Successfully!
"
            "👑 Made by Mr Shivansh
"
            "Ready to Play Music 🎵"
        )

        # Step 9: Idle (keep running)
        try:
            await idle()
        except KeyboardInterrupt:
            LOGGER("SHUKLAMUSIC").info("Stop signal received")
        except Exception as e:
            LOGGER("SHUKLAMUSIC").error(f"Idle error: {e}")

        # Cleanup
        await app.stop()
        await userbot.stop()
        LOGGER("SHUKLAMUSIC").info("Stop Stranger Music Bot")

    except Exception as e:
        LOGGER("SHUKLAMUSIC").error(f"Critical error: {e}")
        raise

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        LOGGER("SHUKLAMUSIC").info("Bot stopped by user")
    except Exception as e:
        LOGGER("SHUKLAMUSIC").error(f"Fatal: {e}")
    finally:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.stop()
        except:
            pass
