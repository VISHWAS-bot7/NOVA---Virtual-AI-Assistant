import datetime
import speech_recognition as sr
import webbrowser
import win32com.client
import pyjokes
import google.generativeai as genai
from config import apikey
import smtplib
from dotenv import load_dotenv
import requests
import os

# Load API Keys from .env file
load_dotenv()

# Store the API keys
gemini_api = os.getenv(apikey)
weather_api = os.getenv('WEATHER_API')
news_api = os.getenv('NEWS_API')


default_location = 'Bangalore, India'


genai.configure(api_key=gemini_api)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=genai.GenerationConfig(
        max_output_tokens=2048,
        temperature=0.7,
    ),
)


speaker = win32com.client.Dispatch("SAPI.spVoice")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            print("Recognizing.....")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some error Occured, Sorry Sir"

def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()

    # Enable low security in gmail
    server.login("your email id", "your email password")
    server.sendmail("your email id", to, content)
    server.close()


def get_weather(city):
    """Fetches weather data and speaks it out."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": weather_api,
        "units": "metric"
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        message = f"The current temperature in {city} is {temp}°C with {weather_desc}."
        print(message)
        speaker.Speak(message)
    else:
        error_msg = "Sorry, I couldn't fetch the weather. Please check the city name."
        print(error_msg)
        speaker.Speak(error_msg)


def get_news():
    print("Fetching news...")  # Debug print
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "in",
        "apiKey": news_api,
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        articles = data["articles"][:5]
        if not articles:
            print("No news articles found.")
            speaker.Speak("I couldn't find any news at the moment.")
            return

        news_list = [f"{idx+1}. {article['title']}" for idx, article in enumerate(articles)]
        news_message = "Here are the top news headlines: " + " ".join(news_list)
        print(news_message)  # Debug print
        speaker.Speak(news_message)
    else:
        print(f"Error fetching news: {response.text}")  # Debug print
        speaker.Speak("Sorry, I couldn't fetch the news.")

while 1:
    s = ("Hello! sir, I am NOVA A I")
    speaker.Speak(s)
    while True:
        print("listening")
        query = takeCommand()
        sites = [["YouTube","https://youtube.com"],["Wikipedia", "https://wikipedia.com"],
                 ["Google", "https://google.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                speaker.Speak(f"Opening {site[0]} sir....")
                webbrowser.open(site[1])
        if "Open music".lower() in query:
            musicpath = "c:Users\Vishw_z89gj1j\Downloads\Salone-296348.mp3"
            os.startfile(musicpath) #CAN CUSTOMIZE IT ACCORDING TO U BY ADDING EXTRA SONGS AND NAMING THEM

        if "the time".lower() in query:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            speaker.Speak(f"Sir the time is {strfTime}")

        #CAN ADD APPS AS WELL JUST LIKE ADDINF MUSIC AND ITS PATH

        if "Using Artificial Intelligence".lower() in query.lower():
            genai(prompt=query)

        elif "NOVA Quit".lower() in query.lower():
            exit()

        elif "Reset Chat".lower() in query.lower():
            chatStr = ""

        elif "Joke".lower() in query.lower():
            joke = pyjokes.get_joke()
            print(joke)
            speaker.Speak(joke)

        elif "Weather".lower() in query.lower():
            city = default_location if not "in" in query else query.split("in")[1].strip()
            get_weather(city)

        elif "News".lower() in query.lower():
            get_news()


        #speaker.Speak(query)