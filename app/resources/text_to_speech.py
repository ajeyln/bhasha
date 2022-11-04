# Import the required module for text 
# to speech conversion 
from gtts import gTTS 

# This module is imported so that we can 
# play the converted audio 
import os 
import time 


def prepare_audio_for_text(wordlist, audioFile, output):
	language = 'de'
	# Passing the text and language to the engine, 
	# here we have marked slow=False. Which tells 
	# the module that the converted audio should 
	# have a high speed 
	# Saving the converted audio in a mp3 file named 
	# welcome 
	with open("resources\pause.mp3", "rb") as pause:
		pauseContent = pause.read()
	
	for item in wordlist:
		myobj = gTTS(text=item, lang=language, slow=False) 
		folder_path = os.path.join(output, audioFile)
		audio_file_path = os.path.join(output, audioFile, f"{item}.mp3")
		pause_audio_file_path = os.path.join(output, audioFile, f"{item}_pause.mp3")
		print(audio_file_path)
		#myobj.save(f"mp3/{audioFile}/{item}.mp3")
		if not os.path.exists(folder_path):
			os.makedirs(folder_path)
		myobj.save(audio_file_path)
		with open(pause_audio_file_path, "wb") as pause:
			pause.write(pauseContent)
