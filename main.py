import random
import time

import speech_recognition as sr
from graphics import *

def draw_frame(swear, window, text, txt):
    if swear:
        window.setBackground(color_rgb(100, 0, 0))
    else:
        window.setBackground(color_rgb(0, 50, 50))
    txt.setText(text)

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

    
TRIGGERS = ['cat', 'dog', 'computer', 'python', 'scheme']
    
# create recognizer and mic instances
recognizer = sr.Recognizer()
microphone = sr.Microphone()

try:
    window = GraphWin("Warning Window", 1000, 900)
    
    txt = Text(Point(500, 100), 'Speak')
    txt.setSize(30)
    txt.setTextColor(color_rgb(255, 255, 255))
    txt.draw(window)

    image = Image(Point(500, 500), 'image-asset.gif')
    image.draw(window)

    draw_frame(False, window, 'Speak', txt)
    while True:
        print("Looking for speech")
        speech = recognize_speech_from_mic(recognizer, microphone)
        
        if speech["transcription"]:
            print(speech["transcription"].lower())
            draw_frame(False, window, speech["transcription"].lower(), txt)
            if speech["transcription"].lower() in TRIGGERS:
                draw_frame(True, window, speech["transcription"].lower(), txt)
                print("Oh no no sir")
        
        if not speech["success"]:
            print("I didn't catch that. What did you say?\n")

        # if there was an error
        if speech["error"]:
            print("ERROR: {}".format(speech["error"]))
    
except KeyboardInterrupt:
    pass
