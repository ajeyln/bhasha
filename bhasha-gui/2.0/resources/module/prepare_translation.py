# https://stackoverflow.com/questions/52455774/googletrans-stopped-working-with-error-nonetype-object-has-no-attribute-group
# https://pypi.org/project/googletrans/
# https://cloud.google.com/translate/docs/languages
#pip uninstall googletrans
# pip install googletrans==4.0.0rc1

from googletrans import Translator
import os
import shutil, sys  


encoding_type='utf-8'
input_folder_name = "input"
output_folder_name_base = "project"

def get_loaded_words(file_path):
    with open(file_path, 'r', encoding=encoding_type) as fileHandle:  
        data = fileHandle.readlines() 
    return [
                item.split("-")[0].strip() or "No response given" for item in data
            ]

def main(source_language = "de", destination_language_1 = "en", destination_languages = ["kn"], inputFolder=".", consoleWriter=""):
    translator = Translator()
    for destination_language_2 in destination_languages :
        output_folder_name = f"{output_folder_name_base}"
        if os.path.exists(output_folder_name):
            shutil.rmtree(output_folder_name)
        if not os.path.exists(output_folder_name):
            os.makedirs(output_folder_name)
        consoleWriter("InfoFunc", f"currently processing for {destination_language_2} language")
        for file in os.listdir(inputFolder):
            dictionary = {}
            consoleWriter("InfoFunc", f"file: {file}")
            file_path = os.path.join(inputFolder, file)
            words = get_loaded_words(file_path)
            consoleWriter("InfoFunc",words)
            baseFileName=f'{file.split(".")[0]}.bhasha'
            for word in words :
                first = translator.translate( text=word, src=source_language, dest= destination_language_1).text
                second = translator.translate( text=word, src=source_language, dest=destination_language_2).text
                dictionary.update ( {
                    f"{word}": f"{first}, {second} "
                }
                )
            output_file = os.path.join(output_folder_name, baseFileName)
            with open(output_file, 'w', encoding=encoding_type, errors='ignore') as normal:
                consoleWriter("InfoFunc", output_file)
                for key in dictionary:
                    normal.write(f"{key} - {dictionary[key]} \n")

if __name__ == '__main__':
    main()

