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
from resources.text_to_speech import prepare_audio_for_text
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


if __name__ == '__main__':

    for file in os.listdir('project/'):
        file_path = os.path.join("project", file)
  
        dictionary = get_loaded_data(file_path)
        baseFileName=f'audio-{file.split(".")[0]}'

# create here all item audio and pause files will be sorted automatically
        print(baseFileName)
        wl = prepare_word_list_with_pause(dictionary)
        #print(wl)
        prepare_audio_for_text(wl, baseFileName, AUDIO_FOLDER_NAME)


# HERE I WANTED TO JOIN ALL THE AUDIO FILES, for now i leave this
# join all the individula mp3 files and prepare final file
    # with open("pause.mp3", "rb") as pause:
        # pauseContent = pause.read()
        # for file in os.listdir(os.path.join(AUDIO_FOLDER_NAME, baseFileName)):
            # file_path = os.path.join(AUDIO_FOLDER_NAME, baseFileName, file) 
            # print(file_path)
            # if not os.path.exists(OUTPUT_FOLDER_NAME):
                # os.makedirs(OUTPUT_FOLDER_NAME)
            # with open(file_path, "rb") as word:
                # with open(os.path.join(OUTPUT_FOLDER_NAME, f"{baseFileName}.mp3"), "wb") as final:
                    # final.write(word.read())
                    #final.write(pauseContent)