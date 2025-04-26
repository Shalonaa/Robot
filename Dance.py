import time
import nxt.locator
from nxt.motor import Motor, PORT_A, PORT_B, PORT_C
from nxt.sensor import Ultrasonic

    #pre-setup: motor B and C in the same location, motor a doesn't matter. Use Calibration.py to change motor rotation before starting.

def main():
    # Connect to the NXT brick
    brick = nxt.locator.find_one_brick()
    
    # Initialize motors
    motor_a = Motor(brick, PORT_A)
    motor_b = Motor(brick, PORT_B)
    motor_c = Motor(brick, PORT_C)
    
    # Reset motor tachometers
    motor_a.reset_position(False)
    motor_b.reset_position(False)
    motor_c.reset_position(False)
    
    # Set initial direction for motor A
    a_direction = 1  # 1 for forward, -1 for backward
    
    # Calculate time for full rotation (360 degrees) at 30% power
    # Empirical value - adjust if needed
    full_rotation_time = 2.5  # seconds
    
    start_time = time.time()
    
    try:
        while True:
            current_time = time.time() - start_time
            
            # Check if we've completed at least one full rotation (motors B and C)
            if current_time >= full_rotation_time:
                break
            
            # Motors B and C at 30% power
            motor_b.run(power=30)
            motor_c.run(power=30)
            
            # Motor A at 50% power, switching direction every 2 seconds
            if int(current_time / 2) % 2 == 0:
                a_direction = 1
            else:
                a_direction = -1
            motor_a.run(power=50 * a_direction)
            
            # Pause motors B and C every 5 seconds
            if int(current_time) % 5 == 0 and int(current_time) > 0:
                motor_b.brake()
                motor_c.brake()
                time.sleep(2)
                # Reset start time after pause to maintain timing
                start_time = time.time() - (current_time % 5)
            
            time.sleep(0.1)  # Small delay to prevent busy waiting
    
    finally:
        # Stop all motors when done
        motor_a.brake()
        motor_b.brake()
        motor_c.brake()

if __name__ == '__main__':
    main()