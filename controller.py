import asyncio
import websockets
import time
import Quartz
from dotenv import load_dotenv
from Quartz.CoreGraphics import CGEventGetLocation, CGDisplayPixelsHigh

load_dotenv()
TARGET_WS = os.getenv("TARGET_WS")

def get_mouse_position():
    loc = Quartz.NSEvent.mouseLocation()
    screen_height = Quartz.CGDisplayPixelsHigh(Quartz.CGMainDisplayID())
    return (int(loc.x), int(screen_height - loc.y))

def get_screen_width():
    return Quartz.CGDisplayPixelsWide(Quartz.CGMainDisplayID())

async def main():
    screen_width = get_screen_width()
    print(f"Connecting to {TARGET_WS}...")
    async with websockets.connect(TARGET_WS) as ws:
        print("Connected.")
        while True:
            x, y = get_mouse_position()
            if x >= screen_width - 1:  # Right edge of screen
                print(f"Sending click at {x}, {y}")
                await ws.send(f"{x},{y}")
                time.sleep(1.5)
            time.sleep(0.01)

asyncio.run(main())
