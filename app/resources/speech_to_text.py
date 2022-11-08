import speech_recognition as sr

r = sr.Recognizer()

def speech_to_text(wordlist):
    language = "de-DE"
    score=0

    for word in wordlist:
        with sr.Microphone() as source:
            print(f"try saying the word {word}")
            audio = r.listen(source)

            try:
                #print("Google Speech Recognition thinks you said " + r.recognize_google(audio, language=language))
                spoken_word = r.recognize_google(audio, language=language)
                if spoken_word.lower() == word.lower():
                    score = score + 1
                    print(f"you pronounced {word} correctly")
                else:
                    print(f"you pronounced {word} incorrectly as {spoken_word}")
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return score, len(wordlist)
