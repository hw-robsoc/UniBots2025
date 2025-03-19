import time
import RPi.GPIO as GPIO

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set up the GPIO pins for the ultrasonic sensors
TRIG_FRONT = 17
ECHO_FRONT = 18

TRIG_LEFT = 22
ECHO_LEFT = 23

TRIG_RIGHT = 24
ECHO_RIGHT = 25

# Set the GPIO pins for trigger as output, echo as input
GPIO.setup(TRIG_FRONT, GPIO.OUT)
GPIO.setup(ECHO_FRONT, GPIO.IN)

GPIO.setup(TRIG_LEFT, GPIO.OUT)
GPIO.setup(ECHO_LEFT, GPIO.IN)

GPIO.setup(TRIG_RIGHT, GPIO.OUT)
GPIO.setup(ECHO_RIGHT, GPIO.IN)

# Set up motor control pins
# Left motor (Motor 1)
IN1 = 5
IN2 = 6
ENA = 13  # Enable pin for PWM (optional)

# Right motor (Motor 2)
IN3 = 19
IN4 = 26
ENB = 21  # Enable pin for PWM (optional)

# Set motor pins as output
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

# Set up PWM for motor speed control (optional)
pwm_left = GPIO.PWM(ENA, 1000)  # 1kHz frequency for left motor speed
pwm_right = GPIO.PWM(ENB, 1000)  # 1kHz frequency for right motor speed
pwm_left.start(100)  # Start with full speed (100% duty cycle)
pwm_right.start(100)  # Start with full speed (100% duty cycle)

def get_distance(trigger_pin, echo_pin):
    # Send a pulse to the trigger pin to start the measurement
    GPIO.output(trigger_pin, GPIO.LOW)
    time.sleep(0.1)
    
    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(0.00001)  # 10us pulse
    GPIO.output(trigger_pin, GPIO.LOW)
    
    # Measure the time taken for the echo to return
    while GPIO.input(echo_pin) == GPIO.LOW:
        pulse_start = time.time()
    
    while GPIO.input(echo_pin) == GPIO.HIGH:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound is 34300 cm/s, so divide by 2 for round trip
    distance = round(distance, 2)
    
    return distance

def move_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    print("Moving Forward")

def move_backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    print("Moving Backward")

def turn_left():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    print("Turning Left")

def turn_right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    print("Turning Right")

def stop_motors():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    print("Motors Stopped")

def check_surroundings():
    # Measure distances from all three sensors
    distance_front = get_distance(TRIG_FRONT, ECHO_FRONT)
    distance_left = get_distance(TRIG_LEFT, ECHO_LEFT)
    distance_right = get_distance(TRIG_RIGHT, ECHO_RIGHT)

    print(f"Front: {distance_front} cm")
    print(f"Left: {distance_left} cm")
    print(f"Right: {distance_right} cm")
    
    # Define a safety threshold (in centimeters)
    safety_distance = 20
    
    # Check if any of the distances are below the safety threshold
    if distance_front < safety_distance:
        print("Warning: Obstacle in front!")
        stop_motors()
        # Optionally, reverse or turn to avoid the obstacle
        move_backward()
        time.sleep(1)
        turn_left()  # Turn left to avoid the obstacle
        time.sleep(1)
    elif distance_left < safety_distance:
        print("Warning: Obstacle on the left!")
        stop_motors()
        # Turn right to avoid the obstacle
        turn_right()
        time.sleep(1)
    elif distance_right < safety_distance:
        print("Warning: Obstacle on the right!")
        stop_motors()
        # Turn left to avoid the obstacle
        turn_left()
        time.sleep(1)
    else:
        move_forward()  # If no obstacle, move forward

def main():
    try:
        while True:
            check_surroundings()
            time.sleep(1)  # Delay between checks
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    finally:
        GPIO.cleanup()  # Clean up GPIO settings

if __name__ == "__main__":
    main()
