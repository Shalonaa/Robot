import time
import random
import nxt.locator
from nxt.motor import Motor, PORT_A, PORT_B, PORT_C
from nxt.sensor import Ultrasonic, PORT_4

    #Working walking code, uses ultrasonic sensor to stop walk state and turn in a random direction. 
    #REQUIRES MOTOR C AND B TO BE SET TO OPPOSITE DIRECTION. Use calibration.py
def main_loop():
    # Connect to the NXT brick
    brick = nxt.locator.find_one_brick()
    
    # Initialize motors
    motor_a = Motor(brick, PORT_A)
    motor_b = Motor(brick, PORT_B)
    motor_c = Motor(brick, PORT_C)
    
    # Initialize ultrasonic sensor
    ultrasonic = Ultrasonic(brick, PORT_4)
    
    # Random walking direction setup
    reverse_motor = random.choice(['B', 'C'])
    print(f"Walking pattern: Motor {reverse_motor} will rotate in opposite direction")
    
    try:
        while True:
            # Check for obstacles
            distance = ultrasonic.get_distance()
            print(f"Distance: {distance} cm")
            
            if distance < 30:  # Obstacle detected within 30cm
                # Stop walking motors
                motor_b.idle()
                motor_c.idle()
                
                # Randomly choose turn direction
                turn_direction = random.choice(['left', 'right'])
                print(f"Obstacle detected! Turning {turn_direction}...")
                
                # Set motor powers based on turn direction (75% power)
                if turn_direction == 'left':
                    motor_b.run(power=-75)  # Left motor backward
                    motor_c.run(power=75)   # Right motor forward
                else:
                    motor_b.run(power=75)   # Left motor forward
                    motor_c.run(power=-75)  # Right motor backward
                
                # Turn for 3 seconds
                time.sleep(3)
                
                # Stop turning
                motor_b.idle()
                motor_c.idle()
                
                # Perform full rotation of motor A
                print("Rotating motor A")
                motor_a.turn(100, 360)
                while motor_a.is_running():
                    time.sleep(0.1)
                
            else:  # No obstacle - continue walking
                # Set power for walking (50% power)
                power_b = -50 if reverse_motor == 'B' else 50
                power_c = -50 if reverse_motor == 'C' else 50
                
                # Start walking (continuous rotation)
                motor_b.run(power=power_b)
                motor_c.run(power=power_c)
                
            time.sleep(0.1)  # Small delay to prevent busy waiting
    
    except KeyboardInterrupt:
        print("Program stopped by user")
    finally:
        # Clean up
        motor_a.idle()
        motor_b.idle()
        motor_c.idle()
        brick.close()

if __name__ == '__main__':
    main_loop()