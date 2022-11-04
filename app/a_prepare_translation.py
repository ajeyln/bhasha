# https://stackoverflow.com/questions/52455774/googletrans-stopped-working-with-error-nonetype-object-has-no-attribute-group
# https://pypi.org/project/googletrans/
# https://cloud.google.com/translate/docs/languages
#pip uninstall googletrans
# pip install googletrans==4.0.0rc1

from googletrans import Translator
import os
import shutil, sys  

encoding_type='utf-8'
source_language = "de"
destination_language_1 = "en"
#destination_languages = ["kn","hi", "ta", "te", "ur", "ml"]
destination_languages = ["kn"]
input_folder_name = "input"
output_folder_name_base = "project"

def get_loaded_words(file_path):
    with open(file_path, 'r', encoding=encoding_type) as fileHandle:  
        data = fileHandle.readlines() 
    return [
                item.split("-")[0].strip() or "No response given" for item in data
            ]

if __name__ == '__main__':
    translator = Translator()


    for destination_language_2 in destination_languages :
        #output_folder_name = f"{output_folder_name_base}-{destination_language_2}"
        output_folder_name = f"{output_folder_name_base}"
        if os.path.exists(output_folder_name):
            shutil.rmtree(output_folder_name)
        if not os.path.exists(output_folder_name):
            os.makedirs(output_folder_name)
        print(f"currently processing for {destination_language_2} language")
        dictionary = {}
        for file in os.listdir(f"{input_folder_name}/"):
            file_path = os.path.join("input", file)
            words = get_loaded_words(file_path)
            print(words)
            baseFileName=f'{file.split(".")[0]}.txt'

            for word in words :
                #pronunciation = translator.translate(word, dest=source_language).pronunciation ##NOT WORKING FOR GERMAN
                first = translator.translate( text=word, src=source_language, dest= destination_language_1).text
                second = translator.translate( text=word, src=source_language, dest=destination_language_2).text
                #third = translator.translate( text=first, src=destination_language_1, dest=destination_language_2).text
                #fourth = translator.translate( text=second, src=destination_language_2, dest=destination_language_1).text
                dictionary.update ( {
                    #f"{word} ? {pronunciation}": f"{first}, {fourth},{second},{third}, " ##NOT WORKING FOR GERMAN
                    f"{word}": f"{first}, {second} "
                }
                )

            #for item in dictionary:
                #print(item)
    
            output_file = os.path.join(output_folder_name, baseFileName)
            with open(output_file, 'w', encoding=encoding_type, errors='ignore') as normal:
                print(output_file)
                for key in dictionary:
                    #word = key.split("?")[0]   ##NOT WORKING FOR GERMAN
                    # pronunciation = key.split("?")[1] ##NOT WORKING FOR GERMAN
                    #normal.write(f"{word} (pronunciation {pronunciation}) - {dictionary[key]} \n")
                    normal.write(f"{key} - {dictionary[key]} \n")