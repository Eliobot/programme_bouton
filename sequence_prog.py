import board
import elio
import time
import digitalio
import neopixel

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
    volume = 50
    elio.playFrequency(523.25, 0.3, volume)  # Do (C)
    time.sleep(0.04)
    elio.playFrequency(659.25, 0.3, volume)  # Mi (E)
    time.sleep(0.04)
    elio.playFrequency(783.99, 0.3, volume)  # Sol (G)
    time.sleep(0.04)


# Function to play end jingle
def play_end_jingle():
    volume = 50
    elio.playFrequency(783.99, 0.3, volume)  # Sol (G)
    time.sleep(0.04)
    elio.playFrequency(659.25, 0.3, volume)  # Mi (E)
    time.sleep(0.04)
    elio.playFrequency(523.25, 0.3, volume)  # Do (C)
    time.sleep(0.04)


# Function definitions for each command
def moveForward():
    pixels.fill((51, 204, 0))
    pixels.show()
    elio.moveOneStep(100)


# Function definitions for each command
def moveBackward():
    pixels.fill((204, 51, 204))
    pixels.show()
    elio.moveBackward(100)
    time.sleep(1)
    elio.motorStop()


def turnRight():
    pixels.fill((51, 102, 255))
    pixels.show()
    elio.turnRight(100)
    time.sleep(0.475)
    elio.motorStop()


def turnLeft():
    pixels.fill((255, 153, 0))
    pixels.show()
    elio.turnLeft(100)
    time.sleep(0.475)
    elio.motorStop()


def stop():
    elio.motorStop()
    pixels.fill((255, 0, 0))  # Red
    pixels.show()


# Function to execute commands
def execute_command(command):
    if command == "Forward":
        moveForward()
    elif command == "Backward":
        moveBackward()
    elif command == "Right":
        turnRight()
    elif command == "Left":
        turnLeft()


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
            print("Repeat finished")
            play_end_jingle()
            time.sleep(0.1)

except KeyboardInterrupt:
    print("Program interrupted")
