from datetime import datetime
import sys
from types import TracebackType
from typing import List, Type

from pyttsx3 import Engine, init
from pyttsx3.voice import Voice
from speech_recognition import Microphone, Recognizer, UnknownValueError

from .database import AssistantDatabase


class Assistant:
	"""The assistant class is the main class of the assistant.
	It contains all the functions and variables that are used in the main program"""

	__slots__ = ("engines", "voices", "recognizer", "database")

	def __init__(self) -> None:
		self.engines: Engine = init("sapi5")
		self.voices: List[Voice] = self.engines.getProperty("voices")
		self.engines.setProperty("voice", self.voices[0].id)
		self.recognizer = Recognizer()
		self.database = AssistantDatabase()

	def wish_me(self) -> None:
		"""Wish me!"""
		if (hour := datetime.now().hour) >= 0 and hour < 12:
			self.speak("Good Morning")

		elif hour >= 12 and hour < 18:
			self.speak("Good Afternoon")

		else:
			self.speak("Good Evening")

	def speak(self, text: str) -> None:
		"""Speak!"""
		self.engines.say(text)
		self.engines.runAndWait()
	
	def recognize_user(self, user: str, password: str) -> None:
		"""Recognize a user."""
		if self.database.recognize_user(user, password):
			self.speak(f"Welcome, {user}")
		
		else:
			self.speak("Password or username incorrect, please try again.")
			sys.exit(1)
	
	def take_command(self) -> str | None:
		"""Take a command."""
		with Microphone() as source:
			self.recognizer.adjust_for_ambient_noise(source)
			self.recognizer.pause_threshold = 1
			print("Listening....")
			audio = self.recognizer.listen(source)

		try:
			query: str = self.recognizer.recognize_google(audio, language="en-in")
			print(f"User Said : {query}\n")

		except UnknownValueError:
			print("Could not understand your voice")
			return

		return query.lower()

	def __enter__(self) -> "Assistant":
		return self

	def __exit__(self,
		exc_type: Type[BaseException] | None = None,
		exc_val: BaseException | None = None,
		exc_tb: TracebackType | None = None
	) -> None:
		pass