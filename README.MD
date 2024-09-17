# P1999 Parser

This script is designed to monitor a log file for specific phrases and play corresponding sound effects when those phrases are detected. It also displays a small, transparent pop-up window with relevant information when triggered. The system is designed for EverQuest Project 1999 (P1999) players to alert them with sound cues and visual notifications when certain game events occur.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [How It Works](#how-it-works)
- [Rule Definitions](#rule-definitions)
- [Customization](#customization)
- [License](#license)

## Requirements

To run this script, you'll need the following:

- Python 3.x
- The following Python libraries:
  - gtts (for text-to-speech)
  - PySimpleGUI (for GUI notifications)
  - subprocess (for playing sounds)
  - re (for regex processing)
  - time (for handling delays and timing)
  - os (for file operations)

You can install the required libraries by running:

pip install gtts PySimpleGUI

## Setup

1. **Log File Location:**
   - Ensure the log file path is correct in the code. The line below should point to your `eqlog` file from P1999:

   with open(r"D:\P1999\Logs\eqlog_Tory_P1999Green.txt", "r") as file:

2. **Sound Files:**
   - Update the `sound_dict` with the correct paths to your sound files. Each sound rule points to a `.wav` file that will be played when triggered.

   sound_dict = {
       'magicCharging': r"D:\P1999\sounds\mail1.wav",
       'alertBloop': r"D:\P1999\sounds\mail2.wav",
       'uhOh': r"D:\P1999\sounds\mail3.wav",
       'fadedUhOh': r"D:\P1999\sounds\mail4.wav",
   }

3. **Pop-up Window Configuration:**
   - The pop-up window uses PySimpleGUI for displaying text. Modify the layout, size, or color as needed:

   layout = [[sg.Text('', key='-TEXT-', background_color=bg, pad=(0, 0))]]
   win = sg.Window('title', layout, no_titlebar=True, keep_on_top=True, location=(900, 900), transparent_color=bg, margins=(0, 0), finalize=True)

## How It Works

- The script follows the P1999 log file in real-time, checking for specific phrases defined in the `rule_dict`. 
- If a matching phrase is detected, a corresponding sound effect from `sound_dict` will play, and the phrase will be displayed in a small, transparent PySimpleGUI window on your screen.

## Rule Definitions

The `rule_dict` contains the phrases to watch for in the log file and the corresponding sound triggers. For example:

rule_dict = {
    'tells you': 'alertBloop',
    'Tory': 'alertBloop',
    'Your spell fizzles!': 'fadedUhOh',
    'Your spell is interrupted.': 'fadedUhOh',
    'Your target resisted the': 'uhOh',
    'Your spell did not take hold': 'uhOh',
    'You feel yourself starting to appear': 'uhOh',
    'spell has worn off': 'magicCharging',
}

When one of these phrases is detected in the log, the appropriate sound effect is played.

## Customization

- **Add New Rules:**
   - To add a new sound alert, simply add an entry to the `rule_dict` and `sound_dict`. Ensure the phrase you're matching is a key in `rule_dict` and points to a sound file in `sound_dict`.
   
   For example, to add an alert for "incoming tell," add this to `rule_dict`:
   
   'incoming tell': 'alertBloop'
   
   And ensure the `sound_dict` contains the sound file:

   'alertBloop': r"D:\P1999\sounds\mail2.wav"

## License

This script is open-source and free to use. Modify it as needed for personal use.
