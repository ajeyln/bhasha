# This file helps German learners to memorize the vocabulary
# Program flashes a word and user must "memorize" the right response
# Program name is inspired by Samskruta word "Charvita Charvana"
# kind of Rote learning
# developed by vazudew

# -*- coding: iso-8859-1 -*-
import codecs
import json
import time
import sys
import os
import random
import shutil
from resources.module.text_to_speech import prepare_audio_for_text
from pydub import AudioSegment
from pydub.playback import play

encoding_type='utf-8'
AUDIO_FOLDER_NAME= "PRACTICE_OUTPUT_FOLDER"
OUTPUT_FOLDER_NAME="PRACTICE_OUTPUT_FOLDER"

def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')

def get_loaded_data(file_path):
    with open(file_path, 'r', encoding=encoding_type) as fileHandle:  
        data = fileHandle.readlines() 
    return {
                item.split("-")[0].strip(): ' '.join(item.split("-")[1:]).strip() or "No response given" for item in data
            }

def prepare_word_list_with_pause(dictionary):
    randomized_dictionary_keys = list(dictionary.keys())
    random.shuffle(randomized_dictionary_keys)
    wordListAsText = ""
    return randomized_dictionary_keys

def get_audio_files(file_path, language, output_folder):
    dictionary = get_loaded_data(file_path)
    baseFileName=f'audio-{file_path.split(os.sep)[-1].split(".")[0]}'
    wl = prepare_word_list_with_pause(dictionary)
    prepare_audio_for_text(wl, baseFileName, output_folder, language)
    
def main():
    for file in os.listdir('project/'):
        file_path = os.path.join("project", file)
        dictionary = get_loaded_data(file_path)
        baseFileName=f'audio-{file.split(".")[0]}'
        wl = prepare_word_list_with_pause(dictionary)
        prepare_audio_for_text(wl, baseFileName, AUDIO_FOLDER_NAME, "de")

if __name__ == '__main__':
    main()


