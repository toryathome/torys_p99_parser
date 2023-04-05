import time
import subprocess
import os
from gtts import gTTS
import re
import PySimpleGUI as sg
import time
import threading
import queue

def display_messages(win, message_queue):
    if not message_queue.empty():
        message = message_queue.get()
        win['-TEXT-'].update(message)
        win.AutoCloseDuration = 4
        win.un_hide()

rule_dict = {
    'tells you': 'alertBloop',
    'Tory': 'alertBloop',
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
    'wtb port': 'alertBloop',
    'lf a port': 'alertBloop',
    'lf port': 'alertBloop',
    'port me to': 'alertBloop',
    'port us to': 'alertBloop',
    'buying port': 'alertBloop',
    'buying a port': 'alertBloop',
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

def follow(file, sleep_sec=0.1):
    line = ''
    while True:
        tmp = file.readline()
        if tmp and len(tmp) > 3:
            line += tmp
            if line.endswith("\n"):
                yield line
                line = ''
        elif sleep_sec:
            time.sleep(sleep_sec)

if __name__ == '__main__':
    message_queue = queue.Queue()
    bg = '#add123'
    sg.set_options(font=("Courier New", 22))
    layout = [[sg.Text('', key='-TEXT-', background_color=bg, pad=(0, 0))]]
    win = sg.Window('title', layout, no_titlebar=True, keep_on_top=True, location=(1100, 900), auto_close=True, auto_close_duration=5, transparent_color=bg, margins=(0, 0), finalize=True)
    win.hide()
    
    with open(r"D:\P1999\Logs\eqlog_Tory_P1999Green.txt", "r") as file:
        file.seek(0, 2)
        for line in follow(file):
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
                    message_queue.put(']'.join(line.split(']')[1:]).split('\n')[0].strip())
            event, values = win.read(timeout=0)
            if event == sg.WIN_CLOSED:
                bg = '#add123'
                sg.set_options(font=("Courier New", 22))
                layout = [[sg.Text('', key='-TEXT-', background_color=bg, pad=(0, 0))]]
                win = sg.Window('title', layout, no_titlebar=True, keep_on_top=True, location=(1100, 900), auto_close=True, auto_close_duration=5, transparent_color=bg, margins=(0, 0), finalize=True)
                win.hide()
            display_messages(win, message_queue)
