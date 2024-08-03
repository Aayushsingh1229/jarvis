import pywhatkit
import speech_recognition as sr
import pyttsx3
import webbrowser
import struct
import pyaudio
import pvporcupine
import os
import datetime
from openai import OpenAI
from access import *
import random
import dateparser
import requests
import sqlite3


# Initialize pyttsx3 engine outside the speak() function
engine = pyttsx3.init()

conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()


def speak(text):
    global engine
    engine.say(text)
    engine.runAndWait()


def image_generation():
    client = OpenAI(api_key=api_key)
    prompt = take_command()
    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    print(image_url)
    webbrowser.open(image_url)


def add_event(title, start_date, end_date, description=""):
    try:
        cursor.execute("INSERT INTO events (title, start_date, end_date, description) VALUES (?, ?, ?, ?)",
                       (title, start_date, end_date, description))
        conn.commit()
        speak("Event added successfully.")
    except sqlite3.Error as e:
        speak("Sorry, I couldn't add the event due to a database error.")
        print(f"Database error: {e}")
    except Exception as e:
        speak("An error occurred while adding the event.")
        print(f"Error: {e}")


def get_weather(city):
    api1_key = api_key1
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api1_key}&q={city}&units=metric"

    response = requests.get(complete_url)
    weather_data = response.json()

    if weather_data['cod'] == 200:
        weather = weather_data['main']
        temperature = weather['temp']
        humidity = weather['humidity']
        weather = weather_data['weather'][0]['description']
        wind_speed = weather_data['wind']['speed']

        weather_report = (f"Temperature: {temperature}°C\n"
                          f"Humidity: {humidity}%\n"
                          f"Weather: {weather}\n"
                          f"Wind Speed: {wind_speed} m/s")
        print(weather_report)
        return weather_report
    else:
        print("City not found.")
        return "I'm sorry, I couldn't find the weather for that location."


def view_events():
    cursor.execute("SELECT title, start_date, end_date, description FROM events")
    for row in cursor.fetchall():
        speak(f"Event: {row[0]}, from {row[1]} to {row[2]}, {row[3]}")


def add_reminder(event_id, reminder_date, message=""):
    cursor.execute("INSERT INTO reminders (event_id, reminder_date, message) VALUES (?, ?, ?)",
                   (event_id, reminder_date, message))
    conn.commit()
    speak("Reminder added successfully.")


def ai(prompt):
    client = OpenAI(
        api_key=api_key
    )
    text = f" openAi response for prompt {prompt}\n *******************\n\n"

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response.choices[0].text)
    text += response.choices[0].text
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"Openai\\prompt- {random.randint(1, 1237236486312)}.txt", "w") as f:
        f.write(text)
    speak(text)


chatStr = ""


def parse_user_date(input_string):
    # Using dateparser to parse the natural language date
    parsed_date = dateparser.parse(input_string)

    if parsed_date:
        # Optionally, format the date to a string or use the datetime object directly
        return parsed_date.strftime('%Y-%m-%d %H:%M:%S')
    else:
        # Handle the case where dateparser can't understand the input
        speak("I couldn't understand the date. Please try again.")
        return None


def chat(query):
    client = OpenAI(api_key=api_key)
    global chatStr
    print(chatStr)
    chatStr = f" User: {query}\n Jarvis:"

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=chatStr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response.choices[0].text)
    speak(response.choices[0].text)
    chatStr += f"{response.choices[0].text}\n"
    return response.choices[0].text


def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 0.5
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Can you please repeat?")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""


# for opening commands


def open_1(query):
    app_name = query.strip()

    if app_name != "":
        try:
            cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening " + query)
                os.startfile(results[0][0])
                return

            cursor.execute('SELECT url FROM web_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening " + query)
                webbrowser.open(results[0][0])
                return
            speak("Opening " + query)
            os.system('start ' + query)
        except Exception as e:
            print(f"Error opening {query}: {e}")
            speak("Sorry, something went wrong")


# the assistant taking the commands

def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)

    return result_string


def contact(query):
    words_to_remove = ['make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?",
                       ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except Exception as e:
        speak(f'An error occurred: {str(e)}')
        return 0, 0


def assistant():
    while True:
        query = take_command()
        if 'play' in query:
            song = query.replace('play', '')
            speak(f'Playing {song} sir')
            pywhatkit.playonyt(song)
            break
        elif 'weather' in query:
            speak("Which city's weather would you like to check?")
            city = take_command()
            if city:
                weather_report = get_weather(city)
                speak(weather_report)
            break
        elif "send message" in query:
            try:
                name, mobile_no = contact(query)
                if mobile_no:
                    speak("What message would you like to send?")

                    message = take_command()
                    if message:
                        pywhatkit.sendwhatmsg_instantly(phone_no='+91' + mobile_no, message=message, wait_time=10)
                        speak("Message sent successfully!")
                        break
                    else:
                        speak("I didn't catch that. Please repeat the message.")
                else:
                    speak("I couldn't find the contact number.")
            except Exception as e:
                speak(f"An error occurred: {str(e)}")
                break
        elif 'open' in query:
            lb = query.replace('open', '')
            open_1(lb)
            break
        elif 'image' in query:
            speak("please give information of the image that you want to  generate")
            image_generation()
            break
        elif 'add event' in query:
            speak("What's the event title?")
            title = take_command()
            speak("What's the start date? Please say it in a way I might understand, like 'tomorrow at 5 PM'.")
            start_date_input = take_command()
            start_date = parse_user_date(start_date_input)

            if start_date is None:
                continue  # Or handle invalid date input appropriately

            speak("What's the end date?")
            end_date_input = take_command()
            end_date = parse_user_date(end_date_input)

            if end_date is None:
                continue  # Or handle invalid date input appropriately
            add_event(title, start_date, end_date, description="")
            break
        elif 'ai' in query:
            speak("Doing sir")
            ai(prompt=query)
            break
        elif 'time' in query:
            time = datetime.datetime.now().strftime('%I:%M %p')
            print(time)
            speak(f'The current time is {time}')
            break
        elif 'search' in query:
            search_query = query.replace('search', '')
            speak(f'Searching for {search_query}')
            pywhatkit.search(search_query)
            break
        elif any(keyword in query for keyword in ['exit', 'goodbye', 'see you later', 'good night', 'bye jarvis']):
            speak("Please wake me if u need anything else!")
            exit()
        else:
            chat(query)


# voice activation


def main():
    print("J.A.R.V.I.S")
    porcupine = None
    paud = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(access_key=access_key, keywords=["jarvis"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True,
                                 frames_per_buffer=porcupine.frame_length)
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            keyword_index = porcupine.process(keyword)
            if keyword_index >= 0:
                speak("Listening sir!")
                assistant()
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


main()
