from elio import Eliobot
import board
import time
import digitalio
import analogio
import pwmio
import neopixel

vBatt_pin = analogio.AnalogIn(board.BATTERY)

obstacleInput = [analogio.AnalogIn(pin) for pin in
                 (board.IO4, board.IO5, board.IO6, board.IO7)]

lineCmd = digitalio.DigitalInOut(board.IO33)
lineCmd.direction = digitalio.Direction.OUTPUT

lineInput = [analogio.AnalogIn(pin) for pin in
             (board.IO10, board.IO11, board.IO12, board.IO13, board.IO14)]

AIN1 = pwmio.PWMOut(board.IO36)
AIN2 = pwmio.PWMOut(board.IO38)
BIN1 = pwmio.PWMOut(board.IO35)
BIN2 = pwmio.PWMOut(board.IO37)

buzzer = pwmio.PWMOut(board.IO17, variable_frequency=True)

elio = Eliobot(AIN1, AIN2, BIN1, BIN2, vBatt_pin, obstacleInput, buzzer, lineInput, lineCmd)

# Built in Neopixel declaration
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2, auto_write=False, pixel_order=neopixel.GRB)

# Define the button pins
buttonForward = digitalio.DigitalInOut(board.IO15)
buttonBackward = digitalio.DigitalInOut(board.IO2)
buttonRight = digitalio.DigitalInOut(board.IO16)
buttonLeft = digitalio.DigitalInOut(board.IO42)
buttonStart = digitalio.DigitalInOut(board.IO39)
buttonStop = digitalio.DigitalInOut(board.IO41)
buttonRepeat = digitalio.DigitalInOut(board.IO40)

# List of all buttons
buttons = [buttonForward, buttonBackward, buttonRight, buttonLeft, buttonStart, buttonStop, buttonRepeat]

for button in buttons:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP

# List to store commands
command_list = []
repeat_list = []
# Variable to keep track of recording status
recording = True

# Dictionary to keep track of button locks
locked = {
    'Forward': False,
    'Backward': False,
    'Right': False,
    'Left': False
}


# Function to play start jingle
def play_start_jingle():
    pixels.fill((0, 255, 0))  # Green
    pixels.show()
    volume = 50
    elio.play_tone(523.25, 0.3, volume)  # Do (C)
    time.sleep(0.04)
    elio.play_tone(659.25, 0.3, volume)  # Mi (E)
    time.sleep(0.04)
    elio.play_tone(783.99, 0.3, volume)  # Sol (G)
    time.sleep(0.04)
    pixels.fill((0, 0, 0))  # Off
    pixels.show()


# Function to play end jingle
def play_end_jingle():
    volume = 50
    elio.play_tone(783.99, 0.3, volume)  # Sol (G)
    time.sleep(0.04)
    elio.play_tone(659.25, 0.3, volume)  # Mi (E)
    time.sleep(0.04)
    elio.play_tone(523.25, 0.3, volume)  # Do (C)
    time.sleep(0.04)


# Function definitions for each command
def move_forward():
    pixels.fill((51, 24, 100)) # Purple
    pixels.show()
    elio.move_forward(100)
    time.sleep(1.6)
    elio.motorStop()
    pixels.fill((0, 0, 0))  # Off
    pixels.show()


# Function definitions for each command
def move_backward():
    pixels.fill((204, 51, 204)) # Pink
    pixels.show()
    elio.move_backward(100)
    time.sleep(1.6)
    elio.motorStop()
    pixels.fill((0, 0, 0))  # Off
    pixels.show()


def turn_right():
    pixels.fill((51, 102, 255)) # Blue
    pixels.show()
    elio.turn_right(100)
    time.sleep(0.415)
    elio.motorStop()
    pixels.fill((0, 0, 0))  # Off
    pixels.show()


def turn_left():
    pixels.fill((255, 153, 0)) # Orange
    pixels.show()
    elio.turn_left(100)
    time.sleep(0.415)
    elio.motorStop()
    pixels.fill((0, 0, 0))  # Off
    pixels.show()


def stop():
    elio.motor_stop()
    pixels.fill((255, 0, 0))  # Red
    pixels.show()


# Function to execute commands
def execute_command(command):
    if command == "Forward":
        move_forward()
    elif command == "Backward":
        move_backward()
    elif command == "Right":
        turn_right()
    elif command == "Left":
        turn_left()


# Main loop
try:
    while True:
        time.sleep(0.1)

        if recording:
            for command, button, lock_key in [('Forward', buttonForward, 'Forward'),
                                              ('Backward', buttonBackward, 'Backward'),
                                              ('Right', buttonRight, 'Right'),
                                              ('Left', buttonLeft, 'Left')]:
                if button.value:
                    if not locked[lock_key]:
                        command_list.append(command)
                        print(f"Recorded {command}")
                        locked[lock_key] = True
                else:
                    locked[lock_key] = False

        # Start command execution
        if buttonStart.value and recording and command_list:
            recording = False
            print("Recording stopped")
            print("Executing commands...")
            play_start_jingle()
            for command in command_list:
                print(f"Executing {command}")
                execute_command(command)
                if buttonStop.value:
                    print("Execution stopped by user")
                    stop()
                    break
                time.sleep(0.3)
            print("Execution finished")
            play_end_jingle()
            repeat_list = command_list
            command_list = []
            recording = True
            time.sleep(0.1)

        # Repeat command execution
        if buttonRepeat.value and recording and repeat_list:
            print("Repeating commands...")
            play_start_jingle()
            for command in repeat_list:
                print(f"Repeating {command}")
                execute_command(command)
                if buttonStop.value:
                    print("Repeat stopped by user")
                    stop()
                    break
                time.sleep(0.3)
            print("Repeat finished")
            play_end_jingle()
            time.sleep(0.1)

except KeyboardInterrupt:
    print("Program interrupted")
