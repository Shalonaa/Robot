import nxt.locator
import nxt.sensor
import time

def main():
    try:
        # Connect to the NXT brick via USB
        brick = nxt.locator.find_one_brick()
        
        # Display "Hello World" on the screen
        brick.message_write(0, 0, "Hello World")
        
        # Wait for 10 seconds
        time.sleep(10)
        
        # Clear the screen before exiting
        brick.message_write(0, 0, " " * 16)  # Clear the line
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Program ended")

if __name__ == "__main__":
    main()