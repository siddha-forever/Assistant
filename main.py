import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
from config import w_apikey
from config import n_apikey
import json
import requests
import datetime
# import customtkinter

chatStr = ""


def alarm(timee):
    current_time = datetime.datetime.now().time().replace(second=0).replace(microsecond=0)
    given_time_obj = datetime.datetime.strptime(timee, "%H:%M").time()

    path = "/Users/siddha-book/PycharmProjects/Assistant/alarm.mp3"
    while (True):
        if current_time == given_time_obj:
            os.system(f"open {path}")
        else:
            break


def news():
    r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={n_apikey}")
    news_data = json.loads(r.content)
    say("Top 5 trending news in India right now is")
    for i in range(5):
        newz = news_data['articles'][i]['title']
        say(newz)


def weatherai(query):
    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={query}&units=imperial&APPID={w_apikey}")

    if weather_data.json()['cod'] == '404':
        print("No City Found")
    else:
        weather = weather_data.json()["weather"][0]["main"]
        temp = round(weather_data.json()['main']['temp'])

        say(f"The weather in {query} is: {weather}")
        say(f"and The temperature is: {temp} degree F")


def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"You: {query}\n Maky: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    try:
        say(response["choices"][0]["text"])
        chatStr += f"{response['choices'][0]['text']}\n"
        return response["choices"][0]["text"]

    except Exception as e:
        return "Some Error Occurred. Sorry from Maky!"


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("OpenAI"):
        os.mkdir("OpenAI")

    with open(f"OpenAI/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)


def say(text):
    os.system(f'say "{text}"')


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
            return "Some Error Occurred. Sorry from Maky"


if __name__ == '__main__':
    say("Hello, welcome to Siddha's Maky A.I System. How can I help you?")
    while True:
        print("Listening...")
        query = takeCommand()

        if "Open".lower() in query.lower():
            # to open a website
            sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                     ["google", "https://www.google.com"], ["instagram", "https://www.instagram.com/"],
                     ["amazon", "https://www.amazon.in/"], ["facebook", "https://www.facebook.com/"]]

            for site in sites:
                if f"Open {site[0]}".lower() in query.lower():
                    say(f"Opening {site[0]}")
                    webbrowser.open(site[1])

            # to open system apps
            # todo : add more app support
            apps = [["Facetime", "/System/Applications/Facetime.app"], ["Clock", "/System/Applications/Clock.app"],
                    ["Messages", "/System/Applications/Messages.app"],
                    ["Weather", "/System/Applications/Weather.app"], ["Chess", "/System/Applications/Chess.app"]]

            for app in apps:
                if f"Open {app[0]}".lower() in query.lower():
                    os.system(f"open {app[1]}")

            # generating delay
            for i in range(2000000000):
                fff = 1

        # playing music
        elif "Play Music".lower() in query.lower():
            musicPath = "/Users/siddha-book/Documents/Python_Work/Music/music.mp3"
            say("playing music")
            os.system(f"open {musicPath}")

        # to ask current time
        elif "The Time".lower() in query.lower():
            t = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"The time is {t}")

        elif "Use Intelligence".lower() in query.lower():
            ai(prompt=query.lower())
            say("Done!")

        elif "weather".lower() in query.lower():
            say("Please tell me the name of your city")
            city = takeCommand()
            weatherai(city)

        elif "news".lower() in query.lower():
            news()

        elif "set alarm".lower() in query.lower():
            say("Please tell the time to set alarm")
            say('Please use 24hour format, for exam 23:01')
            print("Listening...")
            at = takeCommand()
            new_time = at[:2] + ":" + at[2:]
            print(new_time)
            alarm(new_time)
            say("Done!")

        elif "Hey Quit".lower() in query.lower():
            print("Ending Conversation")
            say("Thank you. Have a nice day!!!")
            exit()

        elif "Reset chat".lower() in query.lower():
            chatStr = ""
            say("Chat has been reset")

        else:
            print("Chatting...")
            chat(query)
