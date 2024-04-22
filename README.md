# Elio Robot Command Recorder

This Python script enables the control of an Eliobot using physical buttons to record and execute movement commands such as forward, backward, right, and left turns. The script utilizes a NeoPixel for visual feedback corresponding to different actions and includes the functionality to play jingles at the start and end of command sequences.

## Software Requirements

- CircuitPython firmware installed on your board
- Required CircuitPython libraries:
  - `neopixel`
  - `digitalio`
  - `time`
  - `board`
  - `elio`

## Installation

1. Clone this repository or copy the source code.
2. Ensure your CircuitPython board is connected to your computer.
3. Copy the script into your main.py file (with Thonny or a similar IDE).
4. Restart the board to start the program.

## Usage

- **Recording Commands:**
  - Press the associated buttons to record the commands `Forward`, `Backward`, `Right`, and `Left`.
  - Commands are recorded in sequence as they are input via the buttons.
- **Executing Commands:**
  - Press the `Start` button to stop recording and start executing the recorded commands.
- **Stopping Execution:**
  - During execution, press the `Stop` button to halt further actions.
- **Repeating Commands:**
  - Press the `Repeat` button to execute the last sequence of commands that were executed.

## Note

This script uses locks for the debounce of the button.

## Contribution

Contributions to the project are welcome. Please fork the repository and submit a pull request with your enhancements.
