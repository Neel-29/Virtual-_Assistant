import os
import sys
from datetime import datetime
from pathlib import Path
from webbrowser import BackgroundBrowser, get, register

import requests
import wolframalpha
from wikipedia import summary

from . import Assistant


def main() -> None:
	with Assistant() as assistant:
		assistant.wish_me()
		assistant.speak("Hello Everyone, I am Harry your personal voice assistant, please tell me how I can help you.")
		assistant.speak("Please login with your username.")
		username = assistant.take_command()
		assistant.speak("Password.")
		password = assistant.take_command()
		
		assistant.recognize_user(username, password)

		while True:
			query = assistant.take_command()      # query = anime wikipedia

			if not query:
				break

			if "wikipedia" in query:
				assistant.speak("Searching Wikipedia....")
				query = query.replace("wikipedia", "")    # query = anime ; if we don't use this particular command we will get incorrect info
				query = query.replace(" ", "_")   # it changes the blank spaces to underscore
				results = summary(query, sentences=3)
				print(results)
				assistant.speak(results)

			elif "open youtube" in query:
				register("chrome", None, BackgroundBrowser(r"C:\Program Files\Google\Chrome\Application\chrome.exe"))
				get('chrome').open('https://www.youtube.com/')

			elif "open google" in query:
				register("chrome", None, BackgroundBrowser("C:/Program Files/Google/Chrome/Application/chrome.exe"))
				get('chrome').open('https://www.google.com/')   # if we copy the same elif statement we can open other website also

			elif "search" in query:
				query = query.replace('search ','')
				query = query.replace(' ','+')
				register("chrome", None, BackgroundBrowser("C:/Program Files/Google/Chrome/Application/chrome.exe"))
				get("chrome").open(f"https://www.google.com/search?q={query}")

			elif "play music" in query:
				assistant.speak("Playing music from your playlist......")
				music_directory = Path(__file__).parent / "sounds"
				songs = os.listdir(music_directory)[1]
				os.startfile(music_directory / songs)

			elif "time" in query:
				Current_time = datetime.now().strftime('%I:%M:%S')
				assistant.speak(f'The time is {Current_time}')

			elif "ask a question" in query:
				assistant.speak("It's my pleasure to answer your qustions")
				question = assistant.take_command()
				app_id = 'HTHGRQ-9GLV438L6W'
				client = wolframalpha.Client(app_id)
				res = client.query(question)
				
				for i in res.results:
					print(i.text)
					assistant.speak(i.text)
					
			elif "alarm" in query:
				alarmHour = int(input("Enter Hour:"))
				alarmMin = int(input("Enter Minutes:"))
				alarmAM = input("am/pm:")
				if alarmAM == "pm":
					alarmHour+=12

				while True:
					if alarmHour == datetime.now().hour and alarmMin == datetime.now().minute:
						assistant.speak("Times up")
						music = Path(__file__).parent / "sounds"
						song = os.listdir(music)[0]
						os.startfile(music / song)
						break
			
			elif "weather in" in query:
				city = query.split()[-1]
				api_key = "6eab18419f148afce13a1a2ce985d3f5"
				base_url = 'https://api.openweathermap.org/data/2.5/weather?'

				with requests.get(f"{base_url}q={city}&appid={api_key}&units=metric") as response:
					response.raise_for_status()
					data = response.json()
					assistant.speak(data["main"]["temp"])

			elif "thank you" in query:
				assistant.speak('You are welcome, Have a good day')
				sys.exit(0)

if __name__ == "__main__":
	try:
		main()
	
	except KeyboardInterrupt:
		sys.exit(0)
