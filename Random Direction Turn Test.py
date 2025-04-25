import time
import random
import nxt.locator
from nxt.motor import Motor, PORT_B, PORT_C

	#randomizes direction for the robot to turn 
def rotate_motors_continuously(duration_sec=30):
    # Connect to the NXT brick
    brick = nxt.locator.find_one_brick()
    
    # Initialize motors
    motor_b = Motor(brick, PORT_B)
    motor_c = Motor(brick, PORT_C)
    
    # Randomly choose which motor will rotate in opposite direction
    reverse_motor = random.choice(['B', 'C'])
    print(f"Motor {reverse_motor} will rotate in opposite direction")
    
    # Calculate end time
    end_time = time.time() + duration_sec
    
    try:
        while time.time() < end_time:
            # Set power for each motor (negative for reverse direction)
            power_b = -100 if reverse_motor == 'B' else 100
            power_c = -100 if reverse_motor == 'C' else 100
            
            # Start both motors rotating 360 degrees
            motor_b.turn(power_b, 360)
            motor_c.turn(power_c, 360)
            
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