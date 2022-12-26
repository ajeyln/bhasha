#https://www.geeksforgeeks.org/python-mcq-quiz-game-using-tkinter/

import tkinter as tk
from tkinter import ttk


from tkinter import *
from tkinter import messagebox
from tkinter import messagebox as mb
from tkinter import filedialog
from PIL import ImageTk, Image
import hashlib
import shutil
import webbrowser
from tkhtmlview import *


import json
import os 
import subprocess
import time
from playsound import playsound

from datetime import datetime
from random import randint, shuffle
import zipfile, urllib.request, shutil, time
from resources.module import prepare_translation as pt
from resources.module import prepare_questions as pq
from resources.module import prepare_audio as pa
from resources.module import prepare_speech as ps
from resources.module import prepare_reading as pr
from resources.module.globals import *

#from resources import kwiz
question = {}
options = {}
answer = {}
kwiz = None
audi = None 
pro = None

mcq_xpos = 30
mcq_ypos = 50
kwiz_ypos = 250
audio_ypos = 250

entries=[]
textboxes=[]
answer_key = []
r2_entries=[]
r2_textboxes=[]
r2_answer_key = []
r3_entries=[]
r3_textboxes=[]
r3_answer_key = []


configItems = {}
aboutItems = {}
configFile="bhasha_config.json"
aboutFile ="about.json"
LitFile="literarians.json"

AVOID_CHRACTERS_FILEPATH ="äöüß"
LATEST_UPDATES_URL = "https://github.com/ajeyln/bhasha/releases/download/bhasha-2.0/latest_updates.zip"

## generic

def get_rand_indices(how_many, total):
    return_set = set()
    print(how_many, total)
    while how_many > len(return_set):
        choice=randint(0, total-1)
        if choice not in return_set:
            return_set.add(choice)
    return return_set



#BUTTONS
#MCQ KWIZ 
def mcq_button(ds):
    sets = int(ds.get())
    consoleWrite("Info", f"practice sets needed : {str(sets)}")
    ci = readConfigJson()
    
    if 'outputFolder' in ci.keys():
        consoleWrite("Info", f"output folder : {str(ci['outputFolder'])}")
        root.config(cursor="watch")
        root.update()
        consoleWrite("Info", "MCQ preparation process started")
        time.sleep(1)
        pq.main(PRACTICE_SETS_NEEDED=sets, OUTPUT_FOLDER_NAME=str(ci['outputFolder']), consoleWriter=consoleWrite)
        consoleWrite("Info", "translation process executed")
        root.config(cursor="")
        messagebox.showinfo( "Bhasha", f" completed download files : {sets} sets ")
    else:
        messagebox.showerror( "Bhasha", f" output folder is not configured, please do so in Translate tab ")

def translate_button():
    if len(configItems) == 0:
        messagebox.showerror ("Bhasha", "Please enter configuration items, from 'configure' tab")
        consoleWrite("Err", "Please enter configuration items, from 'configure' tab")
    else: 
        if "focusLanguage" not in configItems or "primaryHelperLanguage" not in configItems or "secondaryHelperLanguage" not in configItems :
            messagebox.showerror ("Bhasha", "Please Language specific configuration items, from 'configure' tab")
            consoleWrite("Err", "Please Language specific configuration items, from 'configure' tab")
        elif "inputWordlistFolder" not in configItems:
            messagebox.showerror ("Bhasha", "Please update wordlist folder, from 'translate' tab")
            consoleWrite("Err", "Please update wordlist folder, from 'translate' tab")
        else:
            Label(tabTranslate, bg='#d9d9d9', font=('Times 14'), text=f"Translated files are located at : {os.path.join(os.getcwd(), 'project')}").place(x=mcq_xpos, y=mcq_ypos+200)
            root.config(cursor="watch")
            root.update()
            consoleWrite("Info", "translation process started")
            time.sleep(1)
            pt.main(source_language = configItems ["focusLanguage"], destination_language_1 = configItems ["primaryHelperLanguage"], 
                destination_languages = [configItems ["secondaryHelperLanguage"]], inputFolder=configItems ["inputWordlistFolder"], 
                consoleWriter=consoleWrite)
            consoleWrite("Info", "translation process executed")
            root.config(cursor="")
            messagebox.showinfo ("Bhasha", "translation finished")

# AUDIO
def prepare_audio(ypos):
    global audi
    ci = readConfigJson()

    if 'outputFolder'  not in ci.keys():
        messagebox.showerror("Bhasha", "output folder is not configured, please do so in Translate tab")
    elif 'inputTranslationFile' not in ci.keys():
        messagebox.showerror("Bhasha", "Input translation file (*.bhasha) is not selected, please do so")
    else:
        op = ci['outputFolder']
        file_path = ci['inputTranslationFile']
        translation_file_base=f'audio-{file_path.split(os.sep)[-1].split(".")[0]}'
        dir_name = os.path.join(op, f"{translation_file_base}")
        #print(f"HERE : {dir_name}")
        if os.path.exists(dir_name):
            if len(os.listdir(dir_name)) != 0:
                consoleWrite("Info", f"audio files already exist : {os.path.join(op, f'{translation_file_base}')}")
                messagebox.showinfo("Bhasha", "audio files exists already")
                
        else :
            consoleWrite("Info", "preparation of audio files started")
            root.config(cursor="watch")
            root.update()
            consoleWrite("Info", f"Audio files will be stored at : {str(ci['outputFolder'])}")
            pa.get_audio_files(ci['inputTranslationFile'], ci['focusLanguage'], ci['outputFolder'])
            root.config(cursor="")
            messagebox.showinfo( "Bhasha", f" completed preparation of audio files ")
        audi=Audio(tabAudio, dir_name, ypos, AVOID_CHRACTERS_FILEPATH)

# READING
def prepare_words(ypos):
    global pro
    ci = readConfigJson()

    if 'outputFolder'  not in ci.keys():
        messagebox.showerror("Bhasha", "output folder is not configured, please do so in Translate tab")
    elif 'inputTranslationFile' not in ci.keys():
        messagebox.showerror("Bhasha", "Input translation file (*.bhasha) is not selected, please do so")
    else:
        op = ci['outputFolder']
        file_path = ci['inputTranslationFile']
        translation_file_base=f'audio-{file_path.split(os.sep)[-1].split(".")[0]}'
        dir_name = os.path.join(op, f"{translation_file_base}")
        #print(f"HERE : {dir_name}")
        #subprocess.call('python', 'hw.py', shell=True)
        image_label.image = tk.PhotoImage(file = '')
        image_label.configure(image=image_label.image)
        status_label.configure(text="")
        pro=Pronounce(tabPronounce, ypos)


def prepare_r1(ypos):
    global entries, textboxes, answer_key, r1_answer_table
    ci = readConfigJson()
    if 'inputReadingFile' not in ci.keys():
        messagebox.showerror("Bhasha", "Input Reading 1 file is not selected, please do so") 
    else:
        if len(textboxes) != 0:
            for i, t in enumerate(textboxes):
                t.destroy()
                entries[i].destroy()
        entries=[]
        textboxes=[]
        answer_key = []
        html_content, options = pr.prepare_html_content(filePath=ci["inputReadingFile"], OUTPUT_FOLDER_NAME=ci["outputFolder"])
        html_label = HTMLLabel(tabGerReading1, bg="#b0e0e6", html=html_content, height=20, width=120)
        html_label.place(x=mcq_xpos, y=mcq_ypos + 200)
        shuffle(options)
        for ind, o in enumerate(options):
            entry=Entry(tabGerReading1, width=2,highlightthickness=2)
            entry.place(x=mcq_xpos+1050, y=mcq_ypos + 200+(80*ind))
            t=Text(tabGerReading1,  font=('Times', '12', 'bold'), wrap=WORD, height = 5,width = 90, bg ="#d9d9d9")
            t.insert(INSERT, f"{ind+1}.{o[0]}")
            t.place(x=mcq_xpos+1100, y=mcq_ypos + 200+(80*ind))
            answer_key.append(o[1])
            textboxes.append(t)
            entries.append(entry)
        if r1_answer_table:
            r1_answer_table.destroy()
            r1_answer_table = Text(tabGerReading1, font=('Times', '12', 'bold'), wrap=WORD, height = 5,width = 20, bg ="#d9d9d9")
            r1_answer_table.tag_configure("left-align", justify='left')
            r1_answer_table.tag_add("left-align", "1.0", "end")
        load_r1_button.configure(state='disabled')
        submit1_button = Button(tabGerReading1,text = "Submit", width=20,bg="#91BAD6",fg="white",font=("ariel",16,"bold"),
            command=lambda: submit(answer_key, submit1_button))
        submit1_button.place(x=mcq_xpos+350, y=mcq_ypos + 570)
        download = Button(tabGerReading1,text = "Download", width=20,bg="#91BAD6",fg="white",font=("ariel",16,"bold"),
            command=lambda: download_r1())
        download.place(x=mcq_xpos+1300, y=mcq_ypos + 570)

def submit(answer_key, submit1_button):
    global entries, r1_answer_table
    score = 0
    r1_answer_table.insert(INSERT, "ANSWER KEY \n\n")
    for ind, e in enumerate(entries) :
        #print(f"E :: {answer_key[ind].lower()} ? O :: {e.get()}")
        if e.get().lower() == answer_key[ind].lower():
            score = score +1
            e.config(highlightbackground = "green", highlightcolor= "green")
        else:
            e.config(highlightbackground = "red", highlightcolor= "red")
        e.configure(state='disabled')
        r1_answer_table.insert(INSERT, f"{ind+1} : {answer_key[ind].lower()} \n")
    r1_answer_table.place(x=mcq_xpos+1150, y=mcq_ypos)
    mb.showinfo("Bhasha", f"Congratulations \n Result : {score*100/len(answer_key)}%\n Correct: {score}\n Wrong: {len(answer_key)-score} ")
    load_r1_button.configure(state='normal')
    submit1_button.configure(state='disabled')


def download_r1():
    ci = readConfigJson()
    pr.download(filePath=ci["inputReadingFile"], OUTPUT_FOLDER_NAME=ci["outputFolder"])
    mb.showinfo("Bhasha", "Reading 1 file has been downloaded into Output folder")

def prepare_r3(ypos):
    global  r3_entries, r3_textboxes, r3_answer_key, r3_answer_table
    ci = readConfigJson()
    if 'inputReading3File' not in ci.keys():
        messagebox.showerror("Bhasha", "Input Reading file is not selected, please do so")   
    else:
        if len(r3_textboxes) != 0:
            for i, t in enumerate(r3_textboxes):
                t.destroy()
                r3_entries[i].destroy()  
        r3_entries=[]
        r3_textboxes=[]
        r3_answer_key = []
        html_content, options = pr.return_classifieds_question(filePath=ci["inputReading3File"])
        html_label = HTMLLabel(tabGerReading3, bg="#b0e0e6", html=html_content, height=20, width=90)
        html_label.place(x=mcq_xpos, y=mcq_ypos + 200)
        shuffle(options)
        for ind, o in enumerate(options):
            entry=Entry(tabGerReading3, width=2,highlightthickness=2)
            t=Text(tabGerReading3,  font=('Times', '12', 'bold'), wrap=WORD, height = 3,width = 50, bg ="#d9d9d9")
            t.insert(INSERT, f"{ind+1}.{o[0]}")
            entry.place(x=mcq_xpos+1050, y=mcq_ypos + 200+(80*(ind+1)))
            t.place(x=mcq_xpos+1100, y=mcq_ypos + 200+(80*(ind+1)))
            r3_answer_key.append(o[1])
            r3_textboxes.append(t)
            r3_entries.append(entry)
    load_r3_button.configure(state='disabled')
    if r3_answer_table:
        r3_answer_table.destroy()
        r3_answer_table = Text(tabGerReading3, font=('Times', '12', 'bold'), wrap=WORD, height = 10,width = 20, bg ="#d9d9d9")
        r3_answer_table.tag_configure("left-align", justify='left')
        r3_answer_table.tag_add("left-align", "1.0", "end")
    submit3_button = Button(tabGerReading3,text = "Submit", width=20,bg="#91BAD6",fg="white",font=("ariel",16,"bold"),
        command=lambda: submit3(r3_answer_key, submit3_button))
    submit3_button.place(x=mcq_xpos+350, y=mcq_ypos + 570)


def prepare_r2(ypos):
    global r2_entries, r2_textboxes, r2_answer_key, r2_answer_table
    ci = readConfigJson()
    if 'inputReadingFile' not in ci.keys():
        messagebox.showerror("Bhasha", "Input Reading file is not selected, please do so") 
    else:
        if len(r2_textboxes) != 0:
            for i, t in enumerate(r2_textboxes):
                t.destroy()
                r2_entries[i].destroy()
        r2_entries=[]
        r2_textboxes=[]
        r2_answer_key = []
        html_content, options = pr.get_r2_html_content(filePath=ci["inputReadingFile"])
        html_label = HTMLLabel(tabGerReading2, bg="#b0e0e6", html=html_content, height=20, width=120)
        html_label.place(x=mcq_xpos, y=mcq_ypos + 200)
        shuffle(options)
        for ind, o in enumerate(options):
            entry=Entry(tabGerReading2, width=2,highlightthickness=2)
            t=Text(tabGerReading2,  font=('Times', '12', 'bold'), wrap=WORD, height = 3,width = 20, bg ="#d9d9d9")
            t.insert(INSERT, f"{ind+1}.{o[0]}")
            if ind%2 == 0 :
                entry.place(x=mcq_xpos+1050, y=mcq_ypos + 200+(20*(ind+1)))
                t.place(x=mcq_xpos+1100, y=mcq_ypos + 200+(20*(ind+1)))
            else:
                entry.place(x=mcq_xpos+1350, y=mcq_ypos + 200+(20*ind))
                t.place(x=mcq_xpos+1400, y=mcq_ypos + 200+(20*ind))
            r2_answer_key.append(o[1])
            r2_textboxes.append(t)
            r2_entries.append(entry)
    load_r2_button.configure(state='disabled')
    if r2_answer_table:
        r2_answer_table.destroy()
        r2_answer_table = Text(tabGerReading2, font=('Times', '12', 'bold'), wrap=WORD, height = 10,width = 20, bg ="#d9d9d9")
        r2_answer_table.tag_configure("left-align", justify='left')
        r2_answer_table.tag_add("left-align", "1.0", "end")
    submit2_button = Button(tabGerReading2,text = "Submit", width=20,bg="#91BAD6",fg="white",font=("ariel",16,"bold"),
        command=lambda: submit2(r2_answer_key, submit2_button))
    submit2_button.place(x=mcq_xpos+350, y=mcq_ypos + 570)


def submit2(answer_key, submit2_button):
    global r2_entries, r2_answer_table
    score = 0
    r2_answer_table.insert(INSERT, "ANSWER KEY \n\n")
    for ind, e in enumerate(r2_entries) :
        if e.get().lower() == answer_key[ind].lower():
            score = score +1
            e.config(highlightbackground = "green", highlightcolor= "green")
        else:
            e.config(highlightbackground = "red", highlightcolor= "red")
        if (ind%2 == 0):
            r2_answer_table.insert(INSERT, f"{ind+1} : {answer_key[ind].lower()} ")
        else: 
            r2_answer_table.insert(INSERT, f"\t  {ind+1} : {answer_key[ind].lower()} \n")
            
        e.configure(state='disabled')
    r2_answer_table.place(x=mcq_xpos+1150, y=mcq_ypos)
    mb.showinfo("Bhasha", f"Congratulations \n Result : {score*100/len(answer_key)}%\n Correct: {score}\n Wrong: {len(answer_key)-score} ")
    load_r2_button.configure(state='normal')
    submit2_button.configure(state='disabled')

def submit3(answer_key, submit3_button):
    global r3_entries, r3_answer_table
    score = 0
    r3_answer_table.insert(INSERT, "ANSWER KEY \n\n")
    for ind, e in enumerate(r3_entries) :
        if e.get().lower() == answer_key[ind].lower():
            score = score +1
            e.config(highlightbackground = "green", highlightcolor= "green")
        else:
            e.config(highlightbackground = "red", highlightcolor= "red")
        r3_answer_table.insert(INSERT, f"{ind+1} : {answer_key[ind].lower()} \n")
        e.configure(state='disabled')
    r3_answer_table.place(x=mcq_xpos+1150, y=mcq_ypos)
    mb.showinfo("Bhasha", f"Congratulations \n Result : {score*100/len(answer_key)}%\n Correct: {score}\n Wrong: {len(answer_key)-score} ")
    load_r3_button.configure(state='normal')
    submit3_button.configure(state='disabled')

# CONFIGURATION
def saveConfig(focus, primary, secondary):
    # if focus, primary and secondary are same ?
    focusL = str(focus.get())
    primaryL = str(primary.get())
    secondaryL = str(secondary.get())
    
    if primaryL.lower() == secondaryL.lower() or focusL.lower() == primaryL.lower() or focusL.lower() == secondaryL.lower():
        messagebox.showerror ("Bhasha", "Please select distinct Focus / Helper languages")
        consoleWrite("Err","Please select distinct Focus / Helper languages")
        
    else :
        #save config items 
        fl = focusL.split("-")[1].strip()
        configItems ["fl"] = focusL
        configItems ["phl"]=primaryL
        configItems ["shl"]=secondaryL
        configItems ["focusLanguage"] = fl
        configItems ["audioFocusLanguage"] = f"{fl}-{fl.upper()}"
        configItems ["primaryHelperLanguage"] = primaryL.split("-")[1].strip()
        configItems ["secondaryHelperLanguage"] = secondaryL.split("-")[1].strip()
        dumpConfigJson()
        consoleWrite("Info","Focus Language : " +  focusL + " Primary Language :" + primaryL + " Secondary Language :" + secondaryL)
        consoleWrite("Info","Configuration Saved.")
        messagebox.showinfo( "Bhasha", "Configuration Saved : \n Focus Language : " +  focusL + "\n Primary Language :" + primaryL + 
            "\n Secondary Language :" + secondaryL )


def setUpConfig(fl="German - de", phl="English - en", shl="Kannada - kn"):
    #font=('Times 14')).place(x=mcq_xpos, y=mcq_ypos)
    ## config language here
    enter = Label(tabConfig, bg='#d9d9d9',text="Language Settings ", font=('Times', '14', 'bold')).place(x=mcq_xpos, y=mcq_ypos)
    Label(tabConfig, bg='#d9d9d9',text="Select your Focus Language",  font=('Times 14')).place(x=mcq_xpos, y=mcq_ypos+100)
    clicked = StringVar()
    clicked.set(fl)
    drop = OptionMenu(tabConfig , clicked, *GOOG_LANG )
    drop.config(width=20)
    drop.config(font=("ariel",14))
    drop.place(x=mcq_xpos+350, y=mcq_ypos+80)
    Label(tabConfig, bg='#d9d9d9',text="Select your Primary Helper Language", font=('Times 14')).place(x=mcq_xpos, y=mcq_ypos+200)
    clickedPHL = StringVar()
    clickedPHL.set(phl)
    dropPHL = OptionMenu(tabConfig , clickedPHL, *GOOG_LANG )
    dropPHL.config(width=20, font=("ariel",14))
    dropPHL.place(x=mcq_xpos+350, y=mcq_ypos+180)
    Label(tabConfig,bg='#d9d9d9', text="Select your Secondary Helper Language",font=('Times 14')).place(x=mcq_xpos, y=mcq_ypos+300)
    clickedSHL = StringVar()
    clickedSHL.set(shl)
    dropSHL = OptionMenu(tabConfig , clickedSHL, *GOOG_LANG )
    dropSHL.config(width=20, font=("ariel",14))
    dropSHL.place(x=mcq_xpos+350, y=mcq_ypos+280)
    # Create button, it will change label text
    button = Button(tabConfig,text = "Save", width=20,bg="#91BAD6",fg="white",font=("ariel",16,"bold"),
        command=lambda: saveConfig(clicked, clickedPHL,clickedSHL ))
    button.place(x=mcq_xpos+350, y=mcq_ypos+400)
    #download latest updates
    download_updates = Button(tabConfig,text = "Download Updates", width=20,bg="#91BAD6",fg="white",font=("ariel",16,"bold"),
        command=lambda: downloadUpdates())
    download_updates.place(x=mcq_xpos+350, y=mcq_ypos+500)

def dumpConfigJson():
    with open(configFile, "w") as fp:
        json.dump(configItems, fp)

def readConfigJson():
    with open(configFile, "r") as fp:
        ci = json.load(fp)
    return ci

def readAboutJson():
    with open(aboutFile, "r") as fp:
        ab = json.load(fp)
    return ab

def readLitJson():
    with open(LitFile, "r", encoding='utf-8') as fp:
        li = json.load(fp)
    return li


def loadConfigFile():
    global input_folder_label
    global output_folder_label
    global input_lable_r1, input_lable_r2, input_lable_r3
    if os.path.isfile(configFile) and os.stat(configFile).st_size != 0:
        consoleWrite("Info", f"{configFile} exist, so loading all the properties")
        ci = readConfigJson()
        setUpConfig(fl=ci["fl"], phl=ci["phl"], shl=ci["shl"])
        if "inputWordlistFolder" in ci.keys() and "outputFolder" in ci.keys() and "inputReadingFile" in ci.keys() and "inputReading3File" in ci.keys():
            input_folder_label.config(text=ci["inputWordlistFolder"])
            output_folder_label.config(text=ci["outputFolder"])
            input_lable_r1.config(text=ci["inputReadingFile"])
            input_lable_r2.config(text=ci["inputReadingFile"])
            input_lable_r3.config(text=ci["inputReading3File"])
            root.update_idletasks()
        return True, ci.copy()
    else:
        ci = {}
        consoleWrite("Info", f"{configFile} does not exist, so loading all fresh")
        ci["inputTranslationFile"] = ""
        return False, ci.copy()

# BROWSE STUFF
def browse_button():
    global input_folder_label
    filename = filedialog.askdirectory()
    if filename :
        configItems ["inputWordlistFolder"] = filename.replace('/', os.sep)
        #configItems ["inputWordlistFolder"] = filename
        dumpConfigJson()
        #print(type(input_folder_label))
        input_folder_label.config(text=filename)
        #Label(tabTranslate, bg='#d9d9d9',text=filename, font=('Times 14')).place(x=mcq_xpos+550, y=mcq_ypos)
        consoleWrite("Info",f"wordlist files will be input from : {filename.replace('/', os.sep)}")
    else:
        consoleWrite("Info","no input folder was selected")

def browseO_button():
    global output_folder_label
    filename = filedialog.askdirectory()
    if filename :
        configItems ["outputFolder"] = filename.replace('/', os.sep)
        dumpConfigJson()
        output_folder_label.config(text=filename)
        consoleWrite("Info",f"output items will be stored at : {filename.replace('/', os.sep)}")
    else: 
        consoleWrite("Info", "no outputfolder was selected")

def downloadUpdates():
    dirname=f'latest-updates-{time.strftime("%Y%m%d-%H%M%S")}'
    updateZipFile = f'{dirname}.zip'
    with urllib.request.urlopen(LATEST_UPDATES_URL) as response, open(updateZipFile, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
        with zipfile.ZipFile(updateZipFile) as zf:
            zf.extractall(dirname)
    os.remove(updateZipFile)
    messagebox.showinfo( "Bhasha", "latest updates are downloaded")

def select_file_reading3(label):
    filetypes = [("JSON Files", '*.json')]
    filename = filedialog.askopenfilename(title='Open a translated file', initialdir='/', filetypes=filetypes)
    if filename:
        configItems ["inputReading3File"] = str(filename).replace('/', os.sep)
        dumpConfigJson()
        consoleWrite("Info", f"selected file : {str(filename).replace('/', os.sep)}")
        label.config(text=configItems["inputReading3File"])
    else: 
        consoleWrite("Info", "no translated file was selected")

def select_file_reading(label):
    filetypes = [("text files", '*.txt')]
    filename = filedialog.askopenfilename(title='Open a translated file', initialdir='/', filetypes=filetypes)
    if filename:
        configItems ["inputReadingFile"] = str(filename).replace('/', os.sep)
        dumpConfigJson()
        consoleWrite("Info", f"selected file : {str(filename).replace('/', os.sep)}")
        label.config(text=configItems["inputReadingFile"])
    else: 
        consoleWrite("Info", "no translated file was selected")
                        
def select_file(ilm, ila):
    filetypes = [("bhasha files", '*.bhasha'), ("text files", '*.txt')]
    filename = filedialog.askopenfilename(title='Open a translated file', initialdir='/', filetypes=filetypes)
    if filename:
        configItems ["inputTranslationFile"] = str(filename).replace('/', os.sep) #filename.split("-")[1].strip()
        #messagebox.showinfo( "Bhasha", f"selected file : {filename}")
        dumpConfigJson()
        consoleWrite("Info", f"selected file : {str(filename).replace('/', os.sep)}")
        ilm.config(text=configItems["inputTranslationFile"])
        ila.config(text=configItems["inputTranslationFile"])
    else: 
        consoleWrite("Info", "no translated file was selected")

#OTHERS
def consoleWrite(mType, message):
    dateTimeObj = datetime.now()
    console.insert("end", f"{dateTimeObj.strftime('%d-%b-%Y (%H:%M:%S.%f)')}{mType} >> {message}")

def callback(event):
    webbrowser.open_new(event.widget.cget("text"))


### GUI STUFF
def highlight(): 
    global kwiz   
    buttons, index = kwiz.get_options_configs()
    answer_index = answer[kwiz.q_no]
    if kwiz.check_ans(kwiz.q_no):
        buttons[index-1].config(bg='#95FFC1')
    else:
        buttons[index-1].config(bg='#FF603B')
        buttons[answer_index-1].config(bg='#95FFC1')
    disableAllButtons(buttons)
    
def show_kwiz(ypos):
    # get the data from the json file
    global question, answer, options, kwiz
    global clickedMode
    configItems ["questionMode"] = str(clickedMode.get())
    dumpConfigJson()
    ci=readConfigJson()
    translated_file = ci['inputTranslationFile']
    mode = ci['questionMode']
    consoleWrite("Info", f" START with translated file : {translated_file} and Mode :{mode}")
    
    question, options, answer = pq.get_qoa(translated_file, mode)
     
    if kwiz is not None :
        kwiz.destroyAllElements() 
    kwiz=Kwiz(tabMCQPlay, ypos) 

def disableAllButtons(buttons):
    for b in buttons:
        b.configure(state='disabled')
    
def setOptionsWhiteBg(buttons):
    for b in buttons :
        b.config(bg='white')

def on_enter(event):
    global audi
    selection = event.widget.curselection()
    audi.focus_word.set(event.widget.get(selection))

def on_pr_enter(event):
    global pro
    selection = event.widget.curselection()
    pro.focus_word.set(event.widget.get(selection))
    image_label.image = tk.PhotoImage(file = '')
    image_label.configure(image=image_label.image)
    status_label.configure(text="")


#CLASSES
class Audio:
    def __init__(self, gui, folder, ypos, chracters_list):

        self.gui = gui 
        self.source_folder = folder 
        self.ypos = ypos
        self.avoided_chracters_in_file_path = chracters_list
        self.wordlist_tracks = self.find_wordlist_tracks()
        self.focus_word = StringVar()#self.wordlist_track[0]
        self.display_title()
        self.display_wordlist_track()
        self.display_audio_player()

    def is_ascii(self, s):
        return all(ord(c) < 128 for c in s)

    def playsound(self):
        current_track =  self.playlist.get(ACTIVE)
        self.focus_word.set(current_track)
        filepath_complete = os.path.join(self.source_folder, current_track)
        #if filehas special characters, then needs to be handled differently !
        if any(c in self.avoided_chracters_in_file_path for c in filepath_complete) or not (self.is_ascii(filepath_complete)):
            temp_folder = os.path.join(self.source_folder, "temp")
            os.makedirs(temp_folder, exist_ok=True)  
            temp_track_name = f"{hashlib.md5(current_track.encode()).hexdigest()}.mp3"
            temp_track_filepath_complete = os.path.join(temp_folder, temp_track_name)
            if not os.path.exists(temp_track_filepath_complete):
                #print("Templ file created")
                shutil.copyfile(filepath_complete, temp_track_filepath_complete)
            playsound(temp_track_filepath_complete)
        else:
            playsound(filepath_complete)
         
    def display_audio_player(self):
        audio_player_frame = LabelFrame(self.gui,text="",font=("times new roman",20,"bold"),bg="white",fg="white",bd=2,relief=GROOVE)
        audio_player_frame.place(x=50, y=self.ypos + 200, width=280,height=50)
        songtrack = Label(audio_player_frame, textvariable=self.focus_word,width=20,font=("times new roman",15,"bold"),
            bg="#E5E7E9",fg="#0E6655").grid(row=0,column=50,padx=10,pady=5)
        button = Button()
        play_button = Button(self.gui, text="Play",command=lambda : self.playsound(),
        width=10,bg="#91BAD6",fg="white",font=("ariel",16,"bold"), state = 'normal')
        # placing the button on the screen
        play_button.place(x=400,y=self.ypos + 200)

        
    def find_wordlist_tracks(self):
        if os.path.exists(self.source_folder):
            return [file for file in os.listdir(self.source_folder) if str(file).lower() != 'temp']
            
    def get_wordlist_tracks(self):
        #print(f"HERE AUDIO: {self.wordlist_tracks}")
        return self.wordlist_tracks
        
    def display_title(self):
        title = Label(self.gui, text="BHASHA Application",
        width=50, bg="#4ADEDE",fg="#990033", font=("ariel", 20, "bold"))
        
        # place of the title
        title.place(x=50, y=self.ypos)
        
    def display_wordlist_track(self):
        songsframe = LabelFrame(self.gui,text="Words Playlist",font=("times new roman",15,"bold"),fg="black",bd=2,relief=GROOVE)
        songsframe.place(x=600,y=self.ypos + 200,width=400,height=200)
        # Inserting scrollbar
        scrol_y = Scrollbar(songsframe,orient=VERTICAL)
        # Inserting Playlist listbox
        self.playlist = Listbox(songsframe,yscrollcommand=scrol_y.set,selectbackground="red",selectmode=SINGLE,
            font=("times new roman",12,"bold"),fg="black",bd=5,relief=GROOVE)
        # Applying Scrollbar to listbox
        scrol_y.pack(side=RIGHT,fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)
        self.playlist.bind("<<ListboxSelect>>", on_enter)
        #self.playlist.bind("<Leave>", on_leave)
        for track in self.get_wordlist_tracks():
            self.playlist.insert(END,track)

class Pronounce :
    def __init__(self, gui, ypos):
        self.gui = gui 
        self.ypos = ypos
        self.wordlist_tracks = self.find_wordlist_tracks()
        self.focus_word = StringVar()#self.wordlist_track[0]
        self.display_title()
        self.display_wordlist_track()
        self.display()


    def checkPronounciation(self):
        current_track =  self.wordlist.get(ACTIVE)
        self.focus_word.set(current_track)
        word, status = ps.check_speech (current_track, readConfigJson()["audioFocusLanguage"])
        image_label.image = tk.PhotoImage(file = 'resources\\images\\wrong.png')
        if status :
            image_label.image = tk.PhotoImage(file = 'resources\\images\\right.png')
        image_label.configure(image=image_label.image)
        image_label.place(x=mcq_xpos+50, y=mcq_ypos +300)
        status_label.configure(text=f" Pronounced word : {word}")

    
    def display(self):
        display_frame = LabelFrame(self.gui,text="",font=("times new roman",20,"bold"),bg="white",fg="white",bd=2,relief=GROOVE)
        display_frame.place(x=50, y=self.ypos + 200, width=280,height=50)
        wordlist = Label(display_frame, textvariable=self.focus_word,width=20,font=("times new roman",15,"bold"),
            bg="#E5E7E9",fg="#0E6655").grid(row=0,column=50,padx=10,pady=5)
        button = Button()
        speak_button = Button(self.gui, text="Pronounce",command=lambda : self.checkPronounciation(), width=10,bg="#91BAD6",
            fg="white",font=("ariel",16,"bold"), state = 'normal')
        # placing the button on the screen
        speak_button.place(x=400,y=self.ypos + 200)
        
    def find_wordlist_tracks(self):
        return ps.get_loaded_data(readConfigJson()['inputTranslationFile'])
            
    def get_wordlist_tracks(self):
        return self.wordlist_tracks
        
    def display_title(self):
        title = Label(self.gui, text="BHASHA Application",
        width=50, bg="#4ADEDE",fg="#990033", font=("ariel", 20, "bold"))
        # place of the title
        title.place(x=50, y=self.ypos)
        
    def display_wordlist_track(self):
        wordframe = LabelFrame(self.gui,text="Words Playlist",font=("times new roman",15,"bold"),fg="black",bd=2,relief=GROOVE)
        wordframe.place(x=600,y=self.ypos + 200,width=400,height=200)
        # Inserting scrollbar
        scrol_y = Scrollbar(wordframe,orient=VERTICAL)
        # Inserting Playlist listbox
        self.wordlist = Listbox(wordframe,yscrollcommand=scrol_y.set,selectbackground="red",selectmode=SINGLE,
            font=("times new roman",12,"bold"),fg="black",bd=5,relief=GROOVE)
        # Applying Scrollbar to listbox
        scrol_y.pack(side=RIGHT,fill=Y)
        scrol_y.config(command=self.wordlist.yview)
        self.wordlist.pack(fill=BOTH)
        self.wordlist.bind("<<ListboxSelect>>", on_pr_enter)
        #self.playlist.bind("<Leave>", on_leave)
        for track in self.get_wordlist_tracks():
            self.wordlist.insert(END,track)


## KWIZ
#class to define the components of the GUI
class Kwiz:
    # This is the first method which is called when a
    # new object of the class is initialized. This method
    # sets the question count to 0. and initialize all the
    # other methoods to display the content and make all the
    # functionalities available
    def __init__(self, gui, ypos):
        global start_button
        start_button.configure(state="disabled")
        # set question number to 0
        self.q_no=0
        self.title_ypos=ypos
        self.gui=gui
        # assigns ques to the display_question function to update later.
        self.display_title()
        self.display_question()
        # opt_selected holds an integer value which is used for
        # selected option in a question.
        self.opt_selected=IntVar()
        # displaying radio button for the current question and used to
        # display options for the current question
        self.opts=self.radio_buttons()
        # display options for the current question
        self.display_options()
        # displays the button for next and exit.
        self.buttons()
        # no of questions
        self.data_size=len(question)
        # keep a counter of correct answers
        self.correct=0

    def destroyAllElements(self):
        for b in self.opts:
            b.destroy()
        self.ql_no.destroy()

    # This method is used to display the result
    # It counts the number of correct and wrong answers
    # and then display them at the end as a message Box
    def display_result(self):
        
        # calculates the wrong count
        wrong_count = self.data_size - self.correct
        correct = f"Correct: {self.correct}"
        wrong = f"Wrong: {wrong_count}"
        
        # calcultaes the percentage of correct answers
        score = int(self.correct / self.data_size * 100)
        result = f"Score: {score}%"
        # Shows a message box to display the result
        mb.showinfo("Bhasha", f"Congratulations \n Result : {result}\n{correct}\n{wrong} ")


    # This method checks the Answer after we click on Next.
    def check_ans(self, q_no):
        # checks for if the selected option is correct
        if self.opt_selected.get() == answer[q_no]:
            #print(f"q: {q_no}, choice: {self.opt_selected.get()}, answ: {answer[q_no]} TRUE")
            return True
        else:
            #print(f"q: {q_no}, choice: {self.opt_selected.get()}, answ: {answer[q_no]} FALSE")
            return False
    # This method is used to check the answer of the
    # current question by calling the check_ans and question no.
    # if the question is correct it increases the count by 1
    # and then increase the question number by 1. If it is last
    # question then it calls display result to show the message box.
    # otherwise shows next question.

    def next_btn(self):
        global start_button
        # Check if the answer is correct
        if self.check_ans(self.q_no):
            # if the answer is correct it increments the correct by 1
            self.correct += 1
        # Moves to next Question by incrementing the q_no counter
        self.q_no += 1
        # checks if the q_no size is equal to the data size
        if self.q_no==self.data_size:
            # if it is correct then it displays the score
            self.display_result()
            # destroys the self.gui
            #self.gui.destroy()
            mb.showerror("Bhasha", "No more questions, load the game again")
            self.next_button.configure(state='disabled')
            start_button.configure(state="normal")
        else:
            # shows the next question
            self.display_question()
            self.display_options()

    # This method shows the two buttons on the screen.
    # The first one is the next_button which moves to next question
    # It has properties like what text it shows the functionality,
    # size, color, and property of text displayed on button. Then it
    # mentions where to place the button on the screen. The second
    # button is the exit button which is used to close the GUI without
    # completing the quiz.
    def buttons(self):
        # The first button is the Next button to move to the
        # next Question
        self.next_button = Button(self.gui, text="Next",command=self.next_btn,
        width=10,bg="#91BAD6",fg="white",font=("ariel",16,"bold"), state = 'normal')
        # placing the button on the screen
        self.next_button.place(x=530,y=self.title_ypos + 250)

    def get_options_configs(self):
        return self.opts, int(str(self.opt_selected.get()))

    # This method deselect the radio button on the screen
    # Then it is used to display the options available for the current
    # question which we obtain through the question number and Updates
    # each of the options for the current question of the radio button.
    def display_options(self):
        val=0
        global options
        # deselecting the options
        self.opt_selected.set(0)
        #print("self qno: {self.q_no}")
        # looping over the options to be displayed for the
        # text of the radio buttons.
        for option in options[self.q_no]:
            self.opts[val]['text']=option
            self.opts[val]['bg']='white'
            self.opts[val]['state']='normal'
            val+=1

    # This method shows the current Question on the screen
    def display_question(self):
        global question
        # setting the Question properties
        self.ql_no = Label(self.gui, text=question[self.q_no], width=60,
        font=( 'ariel' ,16, 'bold' ), anchor= 'w' )
        
        #placing the option on the screen
        self.ql_no.place(x=70, y=self.title_ypos + 70)

    # This method is used to Display Title
    def display_title(self):
        global question
        #print(f"title q : {question}")
        # The title to be shown
        title = Label(self.gui, text="BHASHA Application",
        width=50, bg="#4ADEDE",fg="#990033", font=("ariel", 20, "bold"))
        # place of the title
        title.place(x=50, y=self.title_ypos)

    # This method shows the radio buttons to select the Question
    # on the screen at the specified position. It also returns a
    # list of radio button which are later used to add the options to
    # them.
    def radio_buttons(self):
        # initialize the list with an empty list of options
        q_list = []
        # position of the first option
        y_pos = self.title_ypos + 150
        # adding the options to the list
        while len(q_list) < 4:
            # setting the radio button properties
            radio_btn = Radiobutton(self.gui,text=" ",variable=self.opt_selected,
            value = len(q_list)+1,font = ("ariel",14), bg='white' ,command=lambda : highlight())
            # adding the button to the list
            q_list.append(radio_btn)
            # placing the button
            radio_btn.place(x = 100, y = y_pos)
            # incrementing the y-axis position by 40
            y_pos += 40
        # return the radio buttons
        return q_list

##### GUI STARTS FROM HERE
root = tk.Tk()
root.wm_iconbitmap('resources\\images\\bhasha-icon.ico')
width= root.winfo_screenwidth() #/2         
height= root.winfo_screenheight()#/1.25      
root.geometry("%dx%d" % (width, height))
root.configure(bg="#666633")

s = ttk.Style()
s.theme_create( "MyStyle", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {"configure": {"padding": [50, 10],
                                        "font" : ('URW Gothic L', '11', 'bold')},}})
s.theme_use("MyStyle")
root.title("Bhasha Application")
tabControl = ttk.Notebook(root)

tabConfig = ttk.Frame(tabControl,  width=200, height=200)
tabTranslate = ttk.Frame(tabControl)
tabMCQPlay = ttk.Frame(tabControl)
tabAudio = ttk.Frame(tabControl)
tabPronounce = ttk.Frame(tabControl)
tabGerReading1=ttk.Frame(tabControl)
tabGerReading2=ttk.Frame(tabControl)
tabGerReading3=ttk.Frame(tabControl)
tabAbout = ttk.Frame(tabControl)

tabControl.add(tabConfig, text ='Configure')
tabControl.add(tabTranslate, text ='Translate')
tabControl.add(tabMCQPlay, text ='MCQ Games')
tabControl.add(tabAudio, text ='Audio')
tabControl.add(tabPronounce, text ='Pronunciation')
tabControl.add(tabGerReading1, text ='Reading-1')
tabControl.add(tabGerReading2, text ='Reading-2')
tabControl.add(tabGerReading3, text ='Reading-3')
tabControl.add(tabAbout, text ='About')
tabControl.pack(expand = 1, fill ="both")

scrollbar = Scrollbar(root, orient="vertical")
console = Listbox(root, width=50, height=10, yscrollcommand=scrollbar.set)
scrollbar.config(command=console.yview)
scrollbar.pack(side="right", fill="y")
console.pack(side="left",fill="both", expand=True)
console.configure(background="black", foreground="white", font=('Aerial 13'))

input_folder_label = Label(tabTranslate, bg='#d9d9d9',text="", font=('Times 14'))
output_folder_label=Label(tabTranslate, bg='#d9d9d9',text="", font=('Times 14'))
input_lable_r1=Label(tabGerReading1, bg='#d9d9d9',text="", font=('Times 12'))
input_lable_r2=Label(tabGerReading2, bg='#d9d9d9',text="", font=('Times 12'))
input_lable_r3=Label(tabGerReading3, bg='#d9d9d9',text="", font=('Times 12'))

r1_answer_table = Text(tabGerReading1, font=('Times', '12', 'bold'), wrap=WORD, height = 5,width = 20, bg ="#d9d9d9")
r1_answer_table.tag_configure("left-align", justify='left')
r1_answer_table.tag_add("left-align", "1.0", "end")
r2_answer_table = Text(tabGerReading2, font=('Times', '12', 'bold'), wrap=WORD, height = 10,width = 20, bg ="#d9d9d9")
r2_answer_table.tag_configure("left-align", justify='left')
r2_answer_table.tag_add("left-align", "1.0", "end")
r3_answer_table = Text(tabGerReading3, font=('Times', '12', 'bold'), wrap=WORD, height = 10,width = 20, bg ="#d9d9d9")
r3_answer_table.tag_configure("left-align", justify='left')
r3_answer_table.tag_add("left-align", "1.0", "end")


configLoaded, configItems = loadConfigFile()
if not configLoaded:
    setUpConfig()

## IMAGE PANES FOR TABS !
panes = [tabConfig, tabTranslate, tabMCQPlay, tabAudio, tabPronounce, tabAbout]

literarians = readLitJson()
lit_set_ind = list(get_rand_indices(len(panes), len(literarians)))
img = []

for ind, pane in enumerate(panes):
    Label(pane, bg='#d9d9d9', fg='red', text=f"{literarians[lit_set_ind[ind]]['literarian']}", font=('Times 18')).place(x=mcq_xpos +1300, y=mcq_ypos+50)
    link = Label(pane, font=('Times', '14', 'bold'), text=f"{literarians[lit_set_ind[ind]]['link']}", fg="blue",  cursor="hand2")
    link.place(x=mcq_xpos+1200, y=mcq_ypos+650)
    link.bind("<Button-1>", callback)
    image = ImageTk.PhotoImage(file=literarians[lit_set_ind[ind]]['image'] )
    img.append(image)
    label = Label(pane, image=image)
    label.place(x=mcq_xpos +1200, y=mcq_ypos+100)


##Reading-3
input_lable_r3.place(x=mcq_xpos +200 , y=mcq_ypos +50)
filePicker_r3_Button = Button(tabGerReading3, text='Select a Source File', font=('Times 12'),command=lambda :select_file_reading3(input_lable_r3)) 
filePicker_r3_Button.place(x=mcq_xpos, y=mcq_ypos+ 50)
load_r3_button = Button(tabGerReading3, text="LOAD READING 3",command=lambda: prepare_r3(audio_ypos), 
    width=20,bg="#91BAD6",fg="white",font=("ariel",16,"bold"), state = 'normal')
load_r3_button.place(x=mcq_xpos + 550, y=mcq_ypos + 90)

##Reading-2
input_lable_r2.place(x=mcq_xpos +200 , y=mcq_ypos +50)
filePicker_r2_Button = Button(tabGerReading2, text='Select a Source File', font=('Times 12'),
    command=lambda :select_file_reading(input_lable_r2)) 
filePicker_r2_Button.place(x=mcq_xpos, y=mcq_ypos+ 50)
load_r2_button = Button(tabGerReading2, text="LOAD READING 2",command=lambda: prepare_r2(audio_ypos), 
    width=20,bg="#91BAD6",fg="white",font=("ariel",16,"bold"), state = 'normal')
load_r2_button.place(x=mcq_xpos + 550, y=mcq_ypos + 90)


##Reading-1
input_lable_r1.place(x=mcq_xpos +200 , y=mcq_ypos +50)
filePicker_r1_Button = Button(tabGerReading1, text='Select a Source File', font=('Times 12'),
    command=lambda :select_file_reading(input_lable_r1)) 
filePicker_r1_Button.place(x=mcq_xpos, y=mcq_ypos+ 50)
load_r1_button = Button(tabGerReading1, text="LOAD READING 1",command=lambda: prepare_r1(audio_ypos), 
    width=20,bg="#91BAD6",fg="white",font=("ariel",16,"bold"), state = 'normal')
load_r1_button.place(x=mcq_xpos + 550, y=mcq_ypos + 90)

### About 
ab = readAboutJson()
about_image_label = Label(tabAbout, text = "",bg = '#F4C430') #bg='#d9d9d9')
about_image_label.image = tk.PhotoImage(file = 'resources\\images\\bhasha-icon.png')
about_image_label.configure(image=about_image_label.image)
about_image_label.place(x=mcq_xpos+50, y=mcq_ypos +20)
about_label = Label(tabAbout, bg='#d9d9d9',text=f"{ab['about']}", font=('Times', '16','bold')).place(x=mcq_xpos+300, y=mcq_ypos+20)
version = Label(tabAbout, bg='#d9d9d9',text=f"Version : {ab['version']}",font=('Times', '16','bold')).place(x=mcq_xpos+50, y=mcq_ypos+100)
section_index=0
name_index=0
for section in ['developers', 'contributions', 'supplements']:
    Label(tabAbout, bg='#d9d9d9',text=f"{section.capitalize()}",font=('Times', '16', 'bold')).place(x=mcq_xpos+50, y=mcq_ypos+150*(section_index+1))
    for name in ab[section]:
        Label(tabAbout, text=f"{name.split('>')[0]}",font=('Times', '14'), bg='#d9d9d9').place(x=mcq_xpos+150, y=mcq_ypos+150+50*(name_index+1))
        link = Label(tabAbout, font=('Times', '14', 'bold'), text=f"{name.split('>')[1].strip()}", fg="blue",  cursor="hand2")
        link.place(x=mcq_xpos+400, y=mcq_ypos+150+50*(name_index+1))
        link.bind("<Button-1>", callback)
        name_index = name_index + 1
    section_index = (mcq_ypos+150+(name_index *50))/150-1
    name_index = name_index + 1
        

### PRONOUNCE
Label(tabPronounce, bg='#d9d9d9',text="Select a Translated File ", font=('Times 14')).place(x=mcq_xpos, y=mcq_ypos)
input_lable_wordlist=Label(tabPronounce, bg='#d9d9d9',text=configItems["inputTranslationFile"], font=('Times 12'))
input_lable_wordlist.place(x=mcq_xpos +150 , y=mcq_ypos +50)
filePickerau_Button = Button(tabPronounce, text='Open a translated File', font=('Times 12'),
    command=lambda :select_file(input_lable_wordlist, input_lable_mcq)) 
filePickerau_Button.place(x=mcq_xpos, y=mcq_ypos+ 50)
create_word_button = Button(tabPronounce, text="LOAD WORDS",command=lambda: prepare_words(audio_ypos), 
    width=20,bg="#91BAD6",fg="white",font=("ariel",16,"bold"), state = 'normal')
create_word_button.place(x=mcq_xpos + 550, y=mcq_ypos + 90)
image_label = Label(tabPronounce, text = "",bg='#d9d9d9',)
status_label = Label(tabPronounce, bg='#d9d9d9',text = "", font=('Times 12'))
status_label.place(x=mcq_xpos+150 , y=mcq_ypos +300)


#### AUDIO 
Label(tabAudio, bg='#d9d9d9',text="Select a Translated File ", font=('Times 14')).place(x=mcq_xpos, y=mcq_ypos)
input_lable_audio=Label(tabAudio, bg='#d9d9d9',text=configItems["inputTranslationFile"], font=('Times 12'))
input_lable_audio.place(x=mcq_xpos +150 , y=mcq_ypos +50)
filePickerau_Button = Button(tabAudio, text='Open a translated File', font=('Times 12'), 
    command=lambda :select_file(input_lable_audio, input_lable_mcq)) 
filePickerau_Button.place(x=mcq_xpos, y=mcq_ypos+ 50)
create_audio_button = Button(tabAudio, text="LOAD AUDIO",command=lambda: prepare_audio(audio_ypos), 
    width=20,bg="#91BAD6",fg="white",font=("ariel",16,"bold"), state = 'normal')
create_audio_button.place(x=mcq_xpos + 550, y=mcq_ypos + 90)


# MCQ STUFF here 
Label(tabMCQPlay, bg='#d9d9d9',text="Select a Translated File ", font=('Times 14')).place(x=mcq_xpos, y=mcq_ypos)
input_lable_mcq=Label(tabMCQPlay, bg='#d9d9d9',text=configItems["inputTranslationFile"], font=('Times 12'))
input_lable_mcq.place(x=mcq_xpos +200 , y=mcq_ypos +50)
filePicker_Button = Button(tabMCQPlay, text='Open a translated File', font=('Times 12'),
    command=lambda :select_file(input_lable_mcq, input_lable_audio)) 
filePicker_Button.place(x=mcq_xpos, y=mcq_ypos+ 50)
Label(tabMCQPlay, bg='#d9d9d9',text="Select a mode for questions", font=('Times 14')).place(x=mcq_xpos, y=mcq_ypos+100)
clickedMode = StringVar() # standard, reversed
clickedMode.set(QUESTION_MODE[0])
dropMode = OptionMenu(tabMCQPlay , clickedMode, *QUESTION_MODE)
dropMode.config(width=10)
dropMode.config(font=("ariel",14))
dropMode.place(x=mcq_xpos + 250, y =mcq_ypos+90)
start_button = Button(tabMCQPlay, text="START GAME",command=lambda: show_kwiz(kwiz_ypos), 
    width=10,bg="#91BAD6",fg="white",font=("ariel",16,"bold"), state = 'normal')
start_button.place(x=mcq_xpos + 500, y=mcq_ypos + 90)
enter = Label(tabMCQPlay,bg='#d9d9d9', text="Select how many practice sets you want: ", font=('Times 14'))
enter.place(x=mcq_xpos, y=kwiz_ypos+400)
clickedSet = IntVar()
clickedSet.set(MCQ_SETS[0])
dropSet = OptionMenu(tabMCQPlay , clickedSet, *MCQ_SETS )
dropSet.config(width=5)
dropSet.config(font=("ariel",14))
dropSet.place(x=mcq_xpos + 350, y =kwiz_ypos+400)
mcq = Button(tabMCQPlay, text="Download", font=("ariel",16,"bold"), width=10,bg="#91BAD6",fg="white", 
    command=lambda :mcq_button(clickedSet)).place(x=mcq_xpos+500, y=kwiz_ypos+400)

## TRANSLATE 
enter = Label(tabTranslate, bg='#d9d9d9',text="Select Folder where wordlists are stored  (in plain text): ", font=('Times 14')).place(x=mcq_xpos, y=mcq_ypos)
input_folder_label.place(x=mcq_xpos+650, y=mcq_ypos)
browser = Button(tabTranslate, text="Browse Input Folder",  font=('Times 12'), command=lambda : browse_button()).place(x=mcq_xpos+450, y=mcq_ypos)
enterO = Label(tabTranslate, bg='#d9d9d9',text="Select Folder where output items are stored: ", font=('Times 14')).place(x=mcq_xpos, y=mcq_ypos+100)
output_folder_label.place(x=mcq_xpos+650, y=mcq_ypos+100)
browserO = Button(tabTranslate, text="Browse Output Folder", font=('Times 12'),command=lambda : browseO_button()).place(x=mcq_xpos+450, y=mcq_ypos+100)
translate = Button(tabTranslate, text="Translate", font=("ariel",16,"bold"), width=10,bg="#91BAD6",fg="white", 
    command=translate_button).place(x=mcq_xpos + 450, y=mcq_ypos + 350)

## MAINLOOP
root.mainloop()
