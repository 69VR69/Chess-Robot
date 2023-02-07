import pyttsx3


# Text to speech
def text_to_speech(text, language='fr'):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('voice', language)
    engine.say(text)
    engine.runAndWait()
