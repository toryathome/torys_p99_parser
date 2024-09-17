import time
import subprocess
import os
from gtts import gTTS
import re
import PySimpleGUI as sg
import time
import threading

rule_dict = {
    'tells you': 'alertBloop',
    'Tory': 'alertBloop',
    'Sartorix': 'alertBloop',
    'Toryelus': 'alertBloop',
    'sartori': 'alertBloop',
    'Your spell fizzles!': 'fadedUhOh',
    'Your spell is interrupted.': 'fadedUhOh',
    'Your target resisted the': 'uhOh',
    'Your spell did not take hold': 'uhOh',
    'You feel yourself starting to appear': 'uhOh',
    'spell has worn off': 'magicCharging',
    'tells the group': 'alertBloop',
    'is interested in making a trade': 'alertBloop',
    'adds some coins to the trade': 'alertBloop',
    'shares money with the group': 'alertBloop',
    'invites you to join a group': 'alertBloop',
    'wtb a port': 'alertBloop',
    'potg': 'alertBloop',
    'wtb port': 'alertBloop',
    'lf a port': 'alertBloop',
    'lf port': 'alertBloop',
    'buy a port': 'alertBloop',
    'for a port': 'alertBloop',
    'for port': 'alertBloop',
    'port to': 'alertBloop',
}
sound_dict = {
    'magicCharging': r"D:\P1999\sounds\mail1.wav",
    'alertBloop': r"D:\P1999\sounds\mail2.wav",
    'uhOh': r"D:\P1999\sounds\mail3.wav",
    'fadedUhOh': r"D:\P1999\sounds\mail4.wav",
}

def follow(file, sleep_sec=0.3):
    line = ''
    while True:
        if win.hide_time is not None and time.time() > win.hide_time and win.visible:
            toggle_visibility('OFF', win) 
        _, _ = win.read(timeout=0)
        tmp = file.readline()
        if tmp and len(tmp) > 3:
            line += tmp
            if line.endswith("\n"):
                yield line
                line = ''
        elif sleep_sec:
            time.sleep(sleep_sec)

def toggle_visibility(on_off, win):
    if on_off.upper() == 'OFF':
        win.hide()
        win.visible = False
    elif on_off.upper() == 'ON':
        win.hide_time = time.time() + 6
        win.un_hide()
        win.visible = True

def execute_rule_logic(line):
    for rule in rule_dict:
        if rule.upper() in line.upper():
            if rule == 'Your target resisted the':
                subprocess.Popen(["python", "-m", "playsound", sound_dict[rule_dict[rule]]])
                spell_name = line.split('Your target resisted the')[1].split("spell")[0].strip().replace(" ", "_")
                file_path = f"D:\\tory_files\\pythonCode\\torys_p99_parser\\spell_sounds\\{spell_name}.mp3"
                if not os.path.isfile(file_path):
                    sound_obj = gTTS(text=spell_name.replace("_", " "), slow=False)
                    sound_obj.save(file_path)
                subprocess.Popen(["python", "-m", "playsound", file_path])
            elif rule == 'tells you' and "tells you, 'I'll give you " in line:
                continue
            elif rule == 'spell has worn off':
                pattern = r'\]\sYour\s+(\S+\s*)+spell\s+has\s+worn\s+off'
                matches = re.findall(pattern, line)
                for spell_name in matches:
                    subprocess.Popen(["python", "-m", "playsound", sound_dict[rule_dict[rule]]])
                    spell_name = line.split('Your ')[1].split("spell")[0].strip().replace(" ", "_")
                    file_path = f"D:\\tory_files\\pythonCode\\torys_p99_parser\\spell_sounds\\{spell_name}.mp3"
                    if not os.path.isfile(file_path):
                        sound_obj = gTTS(text=spell_name.replace("_", " "), slow=False)
                        sound_obj.save(file_path)
                    subprocess.Popen(["python", "-m", "playsound", file_path])
            elif rule == 'Tory':
                if 'story' not in line.lower() and 'inventory' not in line.lower():
                    subprocess.Popen(["python", "-m", "playsound", sound_dict[rule_dict[rule]]])
            else:
                subprocess.Popen(["python", "-m", "playsound", sound_dict[rule_dict[rule]]])
            print(line, end='')
            win['-TEXT-'].update(']'.join(line.split(']')[1:]).split('\n')[0].strip())
            win.hide_time = time.time() + 4
            toggle_visibility('ON', win)

if __name__ == '__main__':
    bg = '#add123'
    sg.set_options(font=("Courier New", 24))
    layout = [[sg.Text('', key='-TEXT-', background_color=bg, pad=(0, 0))]]
    win = sg.Window('title', layout, no_titlebar=True, keep_on_top=True, location=(900, 900), transparent_color=bg, margins=(0, 0), finalize=True)
    win.hide()
    win.hide_time = None
    win.visible = False
    with open(r"D:\P1999\Logs\eqlog_Tory_P1999Green.txt", "r") as file:
        file.seek(0, 2)
        while True:
            for line in follow(file):
                execute_rule_logic(line)
                    
                    
           