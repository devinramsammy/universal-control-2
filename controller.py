import asyncio
import websockets
import time
import Quartz
import os
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
    is_controlling_remote = False
    print(f"Connecting to {TARGET_WS}...")
    
    while True:
        try:
            async with websockets.connect(TARGET_WS) as ws:
                print("Connected.")
                last_x, last_y = get_mouse_position()
                
                while True:
                    x, y = get_mouse_position()
                    
                    if x >= screen_width - 1 and not is_controlling_remote:
                        print("Transitioning to remote control")
                        is_controlling_remote = True
                        await ws.send(f"MOVE:0,{y}")
                        time.sleep(0.1)  
                    
                    if is_controlling_remote:
                        dx = x - last_x
                        await ws.send(f"MOVEBY:{dx},{y}")
                    
                    last_x, last_y = x, y
                    time.sleep(0.01)
                    
        except websockets.exceptions.ConnectionClosed:
            print("Connection lost. Reconnecting in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"Error: {e}. Reconnecting in 5 seconds...")
            time.sleep(5)

asyncio.run(main())
