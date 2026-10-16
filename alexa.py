
import os
import datetime
import webbrowser
from urllib.parse import quote_plus

import speech_recognition as sr
import pyttsx3
from groq import Groq


# ---------------- CONFIGURATION ----------------

MODEL_NAME = "openai/gpt-oss-120b"

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("ERROR: Groq API key not found.")
    print("Set GROQ_API_KEY in your terminal, then run this program.")
    raise SystemExit(1)

client = Groq(api_key=api_key)

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 175)

# Initialize speech recognition
recognizer = sr.Recognizer()

# Conversation history
messages = [
    {
        "role": "system",
        "content": (
            "You are Alexa, a helpful AI assistant. "
            "Answer general questions clearly and accurately. "
            "Use simple English unless the user requests otherwise. "
            "Explain coding problems step by step. "
            "If you do not know something, say so honestly."
        )
    }
]


# ---------------- SPEAK ----------------

def speak(text):
    print("\nAlexa:", text)

    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as error:
        print("Voice output error:", error)


# ---------------- LISTEN ----------------

def listen():
    try:
        with sr.Microphone() as source:
            print("\nListening...")

            recognizer.adjust_for_ambient_noise(
                source, duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=20
            )

        question = recognizer.recognize_google(audio)
        print("You:", question)
        return question.strip()

    except sr.WaitTimeoutError:
        print("No speech detected. Please try again.")

    except sr.UnknownValueError:
        print("Sorry, I could not understand. Please repeat.")

    except sr.RequestError as error:
        print("Speech recognition connection error:", error)

    except OSError as error:
        print("Microphone error:", error)
        print("Check your microphone and Windows permissions.")

    return None


# ---------------- AI ANSWERS ----------------

def ask_ai(question):
    messages.append({
        "role": "user",
        "content": question
    })

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.6,
            max_tokens=800
        )

        answer = response.choices[0].message.content

        if not answer:
            answer = "Sorry, I received an empty answer."

        # Save answer for conversation context
        messages.append({
            "role": "assistant",
            "content": answer
        })

        # Keep only recent conversation messages
        if len(messages) > 21:
            messages[:] = [messages[0]] + messages[-20:]

        return answer

    except Exception as error:
        # Remove unanswered user question from history
        if messages and messages[-1]["role"] == "user":
            messages.pop()

        print("\nAI request failed:", error)

        return (
            "Sorry, I could not get an answer from the AI service. "
            "Please check your API key, model availability, "
            "internet connection, and API usage limits."
        )


# ---------------- COMMANDS ----------------

def process_command(question):
    text = question.lower().strip()

    # Exit assistant
    if text in ["exit", "quit", "stop alexa", "goodbye"]:
        speak("Goodbye! Have a great day.")
        return False

    # Current time
    if "time" in text and (
        "what" in text or text == "time"
    ):
        current_time = datetime.datetime.now().strftime(
            "%I:%M %p"
        )
        speak("The current time is " + current_time)
        return True

    # Today's date
    if "date" in text and (
        "what" in text or "today" in text
    ):
        today = datetime.datetime.now().strftime(
            "%d %B %Y"
        )
        speak("Today's date is " + today)
        return True

    # Open websites
    if "open youtube" in text:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")
        return True

    if "open google" in text:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")
        return True

    if "open gmail" in text:
        webbrowser.open("https://mail.google.com")
        speak("Opening Gmail.")
        return True

    # Search the web
    if text.startswith("search for "):
        search_text = question[len("search for "):].strip()

        if search_text:
            url = (
                "https://www.google.com/search?q="
                + quote_plus(search_text)
            )
            webbrowser.open(url)
            speak("Opening Google search results.")
        else:
            speak("Please tell me what you want to search for.")

        return True

    # Answer all other questions using AI
    answer = ask_ai(question)
    speak(answer)

    return True


# ---------------- MAIN PROGRAM ----------------

def main():
    speak("Hello! I am your AI assistant.")
    speak(
        "You can ask me questions about Python, SQL, "
        "Excel, science, or general knowledge."
    )
    speak("Say stop Alexa to exit.")

    while True:
        question = listen()

        if question:
            keep_running = process_command(question)

            if not keep_running:
                break


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nAlexa stopped.")

    except Exception as error:
        print("\nProgram error:", error)
