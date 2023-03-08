import time
from typing import Iterator
import subprocess
import os
from gtts import gTTS

search_text = "say"
rule_dict = {
    'tells you': 'alertBloop',
    'Tory': 'alertBloop',
    'Your spell fizzles!': 'fadedUhOh',
    'Your spell is interrupted.': 'fadedUhOh',
    'Your target resisted the': 'uhOh',
    'You feel yourself starting to appear': 'uhOh',
}
sound_dict = {
    'alertBloop': r"D:\P1999\sounds\mail2.wav",
    'uhOh': r"D:\P1999\sounds\mail3.wav",
    'fadedUhOh': r"D:\P1999\sounds\mail4.wav",
}

def follow(file, sleep_sec=0.1) -> Iterator[str]:
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
        current_position = file.tell()
        file.seek(current_position)

if __name__ == '__main__':
    with open(r"D:\P1999\Logs\eqlog_Tory_P1999Green.txt", "r") as file:
        file.seek(0, 2)
        for line in follow(file):
            for rule in rule_dict:
                if rule.upper() in line.upper():
                    subprocess.Popen(["python", "-m", "playsound", sound_dict[rule_dict[rule]]])
                    if rule == 'Your target resisted the':
                        spell_name = line.split('Your target resisted the')[1].split("spell")[0].strip().replace(" ", "_")
                        file_path = f"D:\\tory_files\\pythonCode\\project_1999_parser\\spell_sounds\\{spell_name}.mp3"
                        if not os.path.isfile(file_path):
                            sound_obj = gTTS(text=spell_name.replace("_", " "), slow=False)
                            sound_obj.save(file_path)
                        subprocess.Popen(["python", "-m", "playsound", file_path])
                    print(line, end='')