# NOVA---Virtual-AI-Assistant

Requirements:

1) datetime
2) speech_recognition as sr
3) webbrowser
4) win32com.client 
5) pyjokes
6) google.generativeai as genai
7) smtplib

Setup

1. API Keys Setup

 a) NOVA requires API keys for weather, news, and AI functionalities.
 b) OpenWeather API (for weather updates)
 c) NewsAPI (for fetching news headlines)
 d) Google Gemini API (for AI responses)

2. Create a .env File

 a) Create a .env file in the project directory and add your API keys:
    
    WEATHER_API=your_openweather_api_key_here
    
    NEWS_API=your_news_api_key_here
    
    API_KEY=your_google_gemini_api_key_here

