import nxt.locator
import nxt.motor
import nxt.sensor
import nxt.sensor.generic
import time

def main():
    # Connect to the NXT brick
    brick = nxt.locator.find_one_brick()

    # Set up motors
    motor_a = nxt.motor.Motor(brick, nxt.motor.Port.A)
    motor_b = nxt.motor.Motor(brick, nxt.motor.Port.B)
    motor_c = nxt.motor.Motor(brick, nxt.motor.Port.C)

    # Set up buttons
    button1 = nxt.sensor.Touch(brick, nxt.sensor.Port.S1)
    button2 = nxt.sensor.Touch(brick, nxt.sensor.Port.S2)

    # Set up ultrasonic sensor
    ultrasonic = nxt.sensor.Ultrasonic(brick, nxt.sensor.Port.S4)

    #initial auto calibration
    try:
        # First part: spin motor B in 30 degree sections until button1 is pressed
        while not button1.get_sample():
            motor_b.turn(30, 50)  # 30 degrees, 50% power
            time.sleep(0.1)  # small delay to prevent overwhelming the motor
        
        time.sleep(1)  # wait 1 second

        # Second part: spin motor C in 30 degree sections until button2 is pressed
        while not button2.get_sample():
            motor_c.turn(30, 50)
            time.sleep(0.1)
        
        time.sleep(3)  # wait 3 seconds

        # Main loop, fine tuning the calibration for specific programs
        while True:
            # Check ultrasonic sensor
            if ultrasonic.get_sample() < 20:  # if something detected within 20cm
                # Motor C loop
                while ultrasonic.get_sample() < 20:
                    motor_c.turn(30, 50)
                    time.sleep(1)  # 1 second delay between turns
                
                # Full rotation of motor A
                motor_a.turn(360, 50)
                time.sleep(2)  # wait 2 seconds

                # Motor B loop
                while ultrasonic.get_sample() < 20:
                    motor_b.turn(30, 50)
                    time.sleep(1)
                
                # Once ultrasonic is no longer covered, exit the program
                break

    finally:
        # Clean up
        motor_a.idle()
        motor_b.idle()
        motor_c.idle()

if __name__ == '__main__':
    main()