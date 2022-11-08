<h1 align="Center"> BHASHA - a language learning app</h1>

## Table of Content

* [Init](#init)
* [Modules](#modules)
* [Provide Input and translate ](#input)
    + [Input file](#ipfile)
    + [Translate](#trans)
* [MCQ - Quiz](#mcq)
* [Spoken words](#audio)
* [ToDos](#todo)
* [Contributions](#contributions)

## <a name="init"></a> Init

There are following 5 items, those needs to be considered

* install Python and related modules : pip install  <b> requirements.txt </b>
* provide input files : here user creates list of words (for exercises) and dumps the file in <b>"input"</b> folder
* prepare translated words for input words : using GOOGLE googletrans package, translated words are prepared in selected source languages
* prepare MCQ Quiz web pages : here Multiple Choice questions contain question word in Target Language and options in Source Languages. Also in order to improve memorization, MCQ web pages are also prepared with Question word in source language and options in Target Language. There is complete randomization on options
* prepare audio files : using GOOGLE gTTS (google text to speech) for any Target Language word, we can create spoken form of the word from native speaker. This helps our learners to listen carefully the words in native form

## <a name="modules"></a> Modules

Bhasha is series of python scripts employed for users to help with language learning. 
We have used HTML/JS based frontend, and GOOGLE SDK for preparing language content. 


Please use python version 3.9 or above

and install following Python modules :

```shell
$ pip install -r requirments.txt
googletrans        4.0.0rc1
gTTS               2.2.4
```
Following scripts are prepared and are to be run alphabetically (please check prefixes)

* app\a_prepare_translation.py
* app\b_prepare_questions.py
* app\c_prepare_audio.py


## <a name="input"></a> Provide Input and Translate

### <a name="ipfile"></a> Input File<br />

First prepare a list of difficult words that you want to learn in Target language. Store these words in a file with distinct name and place it inside the folder <b>input</b>.

Please ensure the words are correctly spelled and with no syntax errors. These words get later translated via googletrans package

![F0](../images/0_input_file.png)

### <a name="trans"></a> Translate <br />

If you want to change target language / source language, please consider setting them in script <i><b>app\a_prepare_translation.py</i></b>. Only [GOOGLE supported languages](https://cloud.google.com/translate/docs/languages) are configurable.

![F1](../images/1_select_language.png)

Now execute the script to prepare translation of all words and files from <b>input</b> folder

```shell
$ python a_prepare_translation.py
```

The resulting translations from GOOGLE will be placed under newly created <b>project</b> folder. This folder is like input for rest of the scripts, as it contains already translations.

![F2](../images/2_prepare_translation.png)
![F3](../images/3_prepare_translation.png)
![F4](../images/4_translated.png)

<b>Please note </b> one can select multiple source languages, but only 1 target language.

## <a name="mcq"></a> MCQ - QUIZ

## <a name="audio"></a> Spoken words audio

## <a name="todo"></a> ToDos
* custom selection of languages
* migrate to cloud 
* database of words list
* end-to-end frontend 
* joining of audio files for exercise
* reading game (fill in the blanks)


## <a name="contribution"></a> Conrtbutions
1 Concept, Design & Development, and Presentation [Vasudeva Nayak Kukkundoor](https://www.linkedin.com/in/vasudeva-nayak-kukkundoor-04183816/) 

2 Devlopment, and Testing [Ajeya Nayak](https://www.linkedin.com/in/ajeya-nayak-34801766/)

3 Frontend design and code [CodingNepal](https://dev.to/codingnepal/create-a-quiz-app-with-timer-using-html-css-javascript-55lf)