import time
import nxt.locator
from nxt.motor import Motor, PORT_B, PORT_C

	#Test code for testing if walk cycle doesn't stop mid rotation (will cause issues with movement if motors aren't synced)
def rotate_motors_continuously(duration_sec=5):
    # Connect to the NXT brick
    brick = nxt.locator.find_one_brick()
    
    # Initialize motors
    motor_b = Motor(brick, PORT_B)
    motor_c = Motor(brick, PORT_C)
    
    # Calculate end time
    end_time = time.time() + duration_sec
    
    try:
        while time.time() < end_time:
            # Start both motors rotating 360 degrees
            motor_b.turn(100, 360)  # 100% power, 360 degrees
            motor_c.turn(100, 360)  # 100% power, 360 degrees
            
            # Wait until both motors complete their rotation
            while motor_b.is_running() or motor_c.is_running():
                time.sleep(0.1)
    
    finally:
        # Stop motors when done or if interrupted
        motor_b.idle()
        motor_c.idle()
        brick.close()

if __name__ == '__main__':
    rotate_motors_continuously(30)