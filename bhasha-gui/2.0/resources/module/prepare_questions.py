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

PRACTICE_SETS_NEEDED = 2
OUTPUT_FOLDER_NAME="PRACTICE_OUTPUT_FOLDER"

encoding_type='utf-8'
def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')

def get_loaded_data(file_path):
    with open(file_path, 'r', encoding=encoding_type) as fileHandle:  
        data = fileHandle.readlines() 
    return {
                item.split("-")[0].strip(): ' '.join(item.split("-")[1:]).strip() or "No response given" for item in data
            }

def return_unique_option(dictionary, question, number_of_options):
    questions = set()
    options = []
    options.append(dictionary[question])
    questions.add(question)
    num_opt = 0
    while (num_opt < number_of_options-1):
        question, option= random.choice(list(dictionary.items()))
        if question not in questions:
            questions.add(question)
            num_opt = num_opt + 1
            options.append(option)

    return random.sample(options, len(options))

def return_unique_option_reverse(dictionary, question, number_of_options):
    questions = set()
    options = []
    options.append(question)
    questions.add(question)
    num_opt = 0

    while (num_opt < number_of_options-1):
        question, option= random.choice(list(dictionary.items()))
        if question not in questions:
            questions.add(question)
            num_opt = num_opt + 1
            options.append(question)
    return random.sample(options, len(options))

def prepare_js_reverse(dictionary, questionFilePath):
    json_value = []
    randomized_dictionary_keys = list(dictionary.keys())
    random.shuffle(randomized_dictionary_keys)
    for i, q in enumerate(randomized_dictionary_keys):
        a = dictionary[q]
        json_value.append( 
          {
            "numb" : i +1,
            "question": a,
            "answer": q,
            "options": return_unique_option_reverse(dictionary, q, 4)
           }
        )
    with open(questionFilePath, 'w') as outfile:
        outfile.write("let questions = ")
        outfile.write(json.dumps(json_value))
        outfile.write(";")

def get_qoa(filename, mode):
    dictionary = get_loaded_data(filename)
    json_value = []
    randomized_dictionary_keys = list(dictionary.keys())
    random.shuffle(randomized_dictionary_keys)
    question = []
    answer   = []
    options = []
    
    if mode.lower() == 'standard':
        for i, q in enumerate(randomized_dictionary_keys):
            question.append(f"{i+1}  {q}")
            ops = return_unique_option(dictionary, q, 4)
            options.append(ops)
            for indx, v in enumerate(ops):
                if v.lower() == dictionary[q].lower():
                    answer.append(indx+1)
                    break
    else: 
        for i, q in enumerate(randomized_dictionary_keys):
            question.append(f"{i+1}  {dictionary[q]}")
            ops = return_unique_option_reverse(dictionary, q, 4)
            options.append(ops)
            for indx, v in enumerate(ops):
                if v.lower() == q.lower():
                    answer.append(indx+1)
                    break
    return question, options, answer

def prepare_htmls(normalPath, reversePath, baseFileName, directory):
    with open("resources/html/source.html") as f:
        htmlCode = f.read()
    with open(f"{directory}/{baseFileName}.html", 'w') as normal:
        normal.write(htmlCode)
        normal.write(f"<script src={normalPath}></script>")
        normal.write("</body></html>")
    with open(f"{directory}/reversed_{baseFileName}.html", 'w') as reverse:
        reverse.write(htmlCode)
        reverse.write(f"<script src={reversePath}></script>")
        reverse.write("</body></html>")

def prepare_js(dictionary, questionFilePath):
    json_value = []
    randomized_dictionary_keys = list(dictionary.keys())
    random.shuffle(randomized_dictionary_keys)
    for i, q in enumerate(randomized_dictionary_keys):
        a = dictionary[q]
        json_value.append( 
          {
            "numb" : i +1,
            "question": q,
            "answer": a,
            "options": return_unique_option(dictionary, q, 4)
           }
        )
    with open(questionFilePath, 'w') as outfile:
        outfile.write("let questions = ")
        outfile.write(json.dumps(json_value))
        outfile.write(";")

def main(PRACTICE_SETS_NEEDED = 2,  OUTPUT_FOLDER_NAME="PRACTICE_OUTPUT_FOLDER", consoleWriter=""):
    for ps in range(PRACTICE_SETS_NEEDED):
        directory=os.path.join(OUTPUT_FOLDER_NAME,f"practice_set{ps}")
        if os.path.exists(directory):
            shutil.rmtree(directory)
        # copy js, style.css, logon.png
        shutil.copytree(os.path.join("resources", "html","js"), os.path.join(directory, "js"))
        shutil.copyfile(os.path.join("resources", "images","a_logo.png"),os.path.join(directory, "a_logo.png"))
        shutil.copyfile(os.path.join("resources", "html","style.css"), os.path.join(directory, "style.css"))
        for file in os.listdir('project/'):
            file_path = os.path.join("project",file)
            consoleWriter("InfoFunc", f"working on file : {file_path}")
            dictionary = get_loaded_data(file_path)
            baseFileName=file.split(".")[0]
            questionFilePath = f"js/{baseFileName}.js"
            questionFilePathReversed =  f"js/{baseFileName}_R.js"
            prepare_js(dictionary, f"{directory}/{questionFilePath}")
            prepare_js_reverse(dictionary,  f"{directory}/{questionFilePathReversed}")
            prepare_htmls(questionFilePath, questionFilePathReversed, baseFileName, directory)

if __name__ == '__main__':
    main()

