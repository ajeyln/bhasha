from gtts import gTTS 
import os 
import time 


def prepare_audio_for_text(wordlist, audioFile, output, language):
	language = language
	for item in wordlist:
		myobj = gTTS(text=item, lang=language, slow=False) 
		folder_path = os.path.join(output, audioFile)
		audio_file_path = os.path.join(output, audioFile, f"{item}.mp3")
		if not os.path.exists(folder_path):
			os.makedirs(folder_path)
		myobj.save(audio_file_path)