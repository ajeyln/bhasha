# This file helps German learners to memorize the vocabulary
# Program flashes a word and user must "memorize" the right response
# Program name is inspired by Samskruta word "Charvita Charvana"
# kind of Rote learning
# developed by vazudew

import json
import time
import sys
import os
import random
import shutil
from resources.module.speech_to_text import *

encoding_type='utf-8'

def get_loaded_data(file_path):
    with open(file_path, 'r', encoding=encoding_type) as fileHandle:  
        data = fileHandle.readlines() 
    return sorted({
                item.split("-")[0].strip(): ' '.join(item.split("-")[1:]).strip() or "No response given" for item in data
            }.keys())

def check_speech(word, language):
    return validate_speech(word, language)

def prepare_word_list(dictionary):
    randomized_dictionary_keys = list(dictionary.keys())
    random.shuffle(randomized_dictionary_keys)
    wordListAsText = ""
    return randomized_dictionary_keys

def main(file_path, language):
    wl = get_loaded_data(file_path)
    baseFileName=f'audio-{file.split(".")[0]}'
    score, total = speech_to_text(wl, language)
    print(f"your pronounced {score} words out of {total} words, CORRECTLY")
    exit()

if __name__ == '__main__':
    file = "C:\\Users\\vazudew\\Desktop\\GITHUB\\tkinter\\app\\project\\second.bhasha"#{sys.argv[1]=}"
    language = "de-DE" 
    main(file, language)