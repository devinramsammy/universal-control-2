import asyncio
import websockets
from Quartz.CoreGraphics import (
    CGEventCreateMouseEvent,
    CGEventPost,
    kCGHIDEventTap,
    kCGEventMouseMoved,
    kCGMouseButtonLeft,
    CGDisplayPixelsWide,
    CGMainDisplayID
)

def get_screen_width():
    return CGDisplayPixelsWide(CGMainDisplayID())

current_x = 0
current_y = 0

def move_mouse(x, y):
    global current_x, current_y
    current_x, current_y = x, y
    event = CGEventCreateMouseEvent(None, kCGEventMouseMoved, (x, y), kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, event)

def move_mouse_by(dx, y):
    global current_x, current_y
    screen_width = get_screen_width()
    new_x = max(0, min(screen_width - 1, current_x + dx))
    move_mouse(new_x, y)

async def handler(websocket):
    global current_x, current_y
    try:
        async for message in websocket:
            try:
                command, coords = message.strip().split(":", 1)
                x_str, y_str = coords.split(",")
                
                if command == "MOVE":
                    x, y = int(x_str), int(y_str)
                    move_mouse(x, y)
                elif command == "MOVEBY":
                    dx, y = int(x_str), int(y_str)
                    move_mouse_by(dx, y)
                
                if current_x <= 0:
                    print("Mouse at left edge - return to MacBook Air")
                
            except ValueError as e:
                print(f"Invalid message format: {message}")
            except Exception as e:
                print(f"Error processing message: {e}")
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    except Exception as e:
        print(f"Handler error: {e}")

async def main():
    print("Starting Universal Control receiver on port 8765...")
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Server started. Waiting for connections...")
        await asyncio.Future() 

if __name__ == "__main__":
    asyncio.run(main())
