import os
import speech_recognition as sr
import pyttsx3

from dotenv import load_dotenv
from groq import Groq

# Load .env file
load_dotenv()

# Get Groq API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("Error: GROQ_API_KEY not found in .env file")
    exit()

# Initialize Groq
client = Groq(api_key=api_key)

# Initialize speech recognizer
recognizer = sr.Recognizer()

user_name = "AADI"
bot_name = "JARVIS"


# Function for JARVIS to speak
def speak(text):
    try:
        engine = pyttsx3.init()

        voices = engine.getProperty("voices")

        if len(voices) > 0:
            engine.setProperty("voice", voices[0].id)

        engine.setProperty("rate", 160) # speed rate

        engine.say(text)
        engine.runAndWait()

        engine.stop()

    except Exception as e:
        print(f"Speech error: {e}")


print("*" * 40)
print("JARVIS Voice Assistant")
print("*" * 40)

# Starting message
speak("Hello Sir. I am ready.")

while True:

    try:

        # Listen to microphone
        with sr.Microphone() as source:

            print("\nListening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=15
            )

        print("No longer listening...")

        # Convert speech to text
        user_input = recognizer.recognize_google(audio)

        print(f"\n{user_name}: {user_input}")

        # Exit commands
        exit_commands = [
         "quit",
         "exit",
         "stop",
         "goodbye",
         "bye",
         "stop jarvis",
         "exit jarvis",
          "goodbye jarvis"
        ]

        if user_input.lower() in exit_commands:

            print(f"You said: {user_input}")
            response_text = "Goodbye Sir . Have a great day!"

            print(f"\n{bot_name}: {response_text}")

            speak(response_text)

            break

        # Send message to Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are JARVIS, a helpful AI voice assistant. "
                        "Give short, clear answers suitable for speaking aloud."
                    )
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            model="llama-3.3-70b-versatile"
        )

        # Get response
        response_text = chat_completion.choices[0].message.content

        print(f"\n{bot_name}: {response_text}")

        # JARVIS speaks every response
        speak(response_text)


    except sr.WaitTimeoutError:
        print("No speech detected. Listening again...")

    except sr.UnknownValueError:
        print("Sorry, I could not understand you.")

    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")

    except Exception as e:
        print(f"Error: {e}")