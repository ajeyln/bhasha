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
from resources.speech_to_text import speech_to_text

encoding_type='utf-8'


def get_loaded_data(file_path):
    with open(file_path, 'r', encoding=encoding_type) as fileHandle:  
        data = fileHandle.readlines() 
    return {
                item.split("-")[0].strip(): ' '.join(item.split("-")[1:]).strip() or "No response given" for item in data
            }

def prepare_word_list(dictionary):
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
        wl = prepare_word_list(dictionary)
        #print(wl)
        score, total = speech_to_text(wl)
        print(f"your pronounced {score} words out of {total} words, CORRECTLY")