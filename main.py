import pyttsx3 #text to speech
import datetime
import speech_recognition as sr
import webbrowser as wb
import pywhatkit
import pyjokes
import pyautogui
import pygame
import requests 
from newsapi import NewsApiClient
import os 
import random
from nltk.sentiment import SentimentIntensityAnalyzer
import openai
from config import apikey


def chat(prompt): #for making the AI to chat
    global chatStr
    chatStr="User said: "+prompt+"\n Jarvis: "   
    openai.api_key=apikey
    
    response = openai.Completion.create(
    model="gpt-3.5-turbo-instruct",
    prompt=chatStr,
    temperature=0.74,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    # print(response["choices"][0]["text"])
    chatStr+=response["choices"][0]["text"]
    return chatStr

def ai(prompt):    #for performing a task using AI
    openai.api_key=apikey
    # print(apikey)

    response = openai.Completion.create(
    model="gpt-3.5-turbo-instruct",
    prompt=prompt,
    temperature=0.74,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open("Openai/" + prompt + ".txt", "w") as f:
        f.write(response["choices"][0]["text"])


def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def greeting():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        say("Good Morning Madam!")
    elif hour >=12 and hour < 18:
        say("Good Afternoon Madam!")
    elif hour >=18 and hour < 24:
        say("Good Evening Madam!")
    else:
        say("Good Night!")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source: 
        # r.pause_threshold =  0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"

def takeScreenshot():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot = pyautogui.screenshot() #capture ss
    screenshot.save(f"screenshot_{timestamp}.png") #saves ss
    say("Screenshot saved")

pygame.mixer.init()
# Function to get a list of music files in the directory
def get_music_files(directory):
    music_files = [f for f in os.listdir(directory) if f.endswith(('.mp3', '.wav', '.ogg'))]
    return music_files

# Function to play a random music file from the Music folder
def play_random_music():
    music_folder = os.path.join(os.environ['HOMEPATH'], 'Music')
    
    # Check if the Music folder exists
    if os.path.exists(music_folder):
        # Get a list of all files in the Music folder
        music_files = get_music_files(music_folder)
        
        if music_files:
            # Choose a random music file
            chosen_music = os.path.join(music_folder, random.choice(music_files))
            
            # Play the chosen music
            pygame.mixer.music.load(chosen_music)
            pygame.mixer.music.play()
            say("Playing Music")
        else:
            say("No music files found in the Music folder.")
    else:
        say("Music folder not found. Please check the path.")

music_playing = False


def toggle_music():
    global music_playing
    
    if music_playing:
        pygame.mixer.music.stop()
        say("Music Stopped")
    else:
        play_random_music()
    
    # Toggle the music status
    music_playing = not music_playing


def get_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    # Get a compound sentiment score between -1 (negative) and 1 (positive)
    sentiment_score = sid.polarity_scores(text)['compound']
    
    if sentiment_score >= 0.05:
        return "positive"
    elif sentiment_score <= -0.05:
        return "negative"
    else:
        return "neutral" 


if __name__ == '__main__':
    say("I am JARVIS, your Virtual Artificial Intelligence")
    greeting()
    say("JARVIS at your service, please tell me how can I help you?")
    
    while True:
        query = takeCommand().lower()

        if 'time' in query:
            hr = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Madam time is {hr} bajke {minute}")

        elif 'remember' in query:
            say("What do you want me to remember?")
            data = takeCommand()
            say("You told me to remember that " +data)
            remember = open('data.txt','a')
            remember.write(data+'\n')

        elif 'know anything' in query:
            remember = open('data.txt','r')
            say("You told me to remember that " +remember.read())

        elif 'camera' in query:
            camera_url = 'microsoft.windows.camera:'
            wb.open(camera_url)

        elif 'youtube' in query:
            say("What should i search on youtube?")
            topic = takeCommand()
            pywhatkit.playonyt(topic)

        elif 'search' in query:
            say("What should i search on google?")
            search = takeCommand()
            wb.open('https://www.google.com/search?q='+search)

        elif 'instagram' in query:
            say("Opening instagram")
            wb.open('wwww.instagram.com')

        elif 'screenshot' in query:
            takeScreenshot()

        elif 'music' in query:
            toggle_music()

        elif 'how' in query:
            mood = get_sentiment(query)
            if mood == "positive":
                say("I'm doing well, thank you!")
            elif mood == "negative":
                say("I'm sorry to hear that. Is there anything I can do to help?")
            else:
                say("I'm doing fine, thanks for asking!")

        elif 'offline' in query or 'bye' in query:
            say("Thank you! Goodbye")
            quit()
        elif 'using artificial intelligence'.lower() in query.lower():
            ai(prompt=query)
        else:
            print("Chatting....")
            say(chat(query))