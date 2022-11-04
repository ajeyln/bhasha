import sys
import os	

from pydub import AudioSegment
from pydub.playback import play




if __name__ == '__main__':

	with open("pause.mp3", "rb") as pause:
		pauseContent = pause.read()
	
	folderLoc=f"mp3/{folder}/"
	for file in os.listdir(folderLoc):
		file_path = f"mp3/{folder}/{file}" 
		print(file_path)

		with open(file_path, "rb") as word:
			with open("vazu.mp3", "wb") as final:
				final.write(word.read())
				final.write(pauseContent)