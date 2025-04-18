import asyncio
import websockets
from Quartz.CoreGraphics import (
    CGEventCreateMouseEvent,
    CGEventPost,
    kCGHIDEventTap,
    kCGEventLeftMouseDown,
    kCGEventLeftMouseUp,
    kCGMouseButtonLeft
)

def click(x, y):
    for event_type in [kCGEventLeftMouseDown, kCGEventLeftMouseUp]:
        event = CGEventCreateMouseEvent(None, event_type, (x, y), kCGMouseButtonLeft)
        CGEventPost(kCGHIDEventTap, event)

async def handler(websocket):
    async for message in websocket:
        try:
            x_str, y_str = message.strip().split(",")
            x, y = int(x_str), int(y_str)
            print(f"Clicking at {x}, {y}")
            click(x, y)
        except Exception as e:
            print("Error:", e)

async def main():
    print("Waiting for connection on port 8765...")
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()  # Run forever

asyncio.run(main())
