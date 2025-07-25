import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser
import time
import random

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

reminders = []

def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():    
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', "")
                print(command)
            return command
    except sr.WaitTimeoutError:
        print("Listening timed out while waiting for phrase to start.")
        return ""
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""

def rock_paper_scissors():
    choices = ['rock', 'paper', 'scissors']
    assistant_choice = random.choice(choices)
    talk("Let's play Rock, Paper, Scissors. Make your choice.")
    user_choice = take_command()
    if user_choice in choices:
        talk(f"I chose {assistant_choice}.")
        if user_choice == assistant_choice:
            talk("It's a tie!")
        elif (user_choice == 'rock' and assistant_choice == 'scissors') or \
             (user_choice == 'paper' and assistant_choice == 'rock') or \
             (user_choice == 'scissors' and assistant_choice == 'paper'):
            talk("You win!")
        else:
            talk("I win!")
    else:
        talk("That's not a valid choice.")


def number_guessing_game():
    number = random.randint(1, 100)
    talk("I have thought of a number between 1 and 100. Can you guess it?")
    attempts = 0
    while True:
        try:
            guess = int(take_command())
            attempts += 1
            if guess < number:
                talk("Too low. Try again.")
            elif guess > number:
                talk("Too high. Try again.")
            else:
                talk(f"Congratulations! You guessed it in {attempts} attempts.")
                break
        except ValueError:
            talk("Please say a number.")



def set_alarm(alarm_time):
    current_time = datetime.datetime.now().strftime('%H:%M')
    while current_time != alarm_time:
        time.sleep(1)
        current_time = datetime.datetime.now().strftime('%H:%M')
    talk("It's time to wake up!")
    print("Alarm ringing!")



def add_reminder(reminder):
    reminders.append(reminder)
    return "Reminder added."

def run_alexa():
    command = take_command()
    if command:
        if 'play' in command:
            song = command.replace('play', )
            print('playing'+song)
            talk('Playing ' + song)
            pywhatkit.playonyt(song)
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            print(time)
            talk('The current time is ' + time)
        elif 'date' in command:
            time= datetime.datetime.now().strftime("%B %d, %Y")
            print(time)
            talk('The current time is ' + time)

        elif "open google" in command:
            talk("Here you go to Google")   
            webbrowser.open("https://google.com") 
        elif "open wikipedia" in command:
            talk("here you go to wekepia")
            webbrowser.open("https://wikipedia.com")    
        elif 'who is' in command:
            person = command.replace("who is", " ").strip()  
            info = wikipedia.summary(person, 1) 
            talk(info)
            print(info)
        elif 'weather in' in command:
            location = command.replace('weather in', '').strip()
            talk(f"Let me check the weather in {location}.")
            webbrowser.open(f"https://www.google.com/search?q=weather+in+{location}")
        
        elif 'set alarm for' in command:
         alarm_time = command.replace('set alarm for', '').strip()
         talk(f"Setting an alarm for {alarm_time}.")
         set_alarm(alarm_time) 
            

        elif "joke" in command:
            joke=(pyjokes.get_joke())
            print(joke)
            talk(joke)
        elif "hi" in command:
            greeting = "Hi! Is there something I can help you with?"
            print(greeting)   
            talk(greeting) 
        elif "open youtube" in command:
            talk("Here you go to YouTube")
            webbrowser.open("https://youtube.com")
        elif 'remind me to' in command:
            reminder = command.replace('remind me to', '').strip()
            response = add_reminder(reminder)
            talk(response)
            print(response)
            
        
        elif 'what are my reminders' in command:
            if reminders:
                reminder_text = "Here are your reminders: " + "; ".join(reminders)
            else:
                reminder_text = "You have no reminders."
            talk(reminder_text)
            print(reminder_text)

        
        elif 'switch to game' in command:
            talk("Which game would you like to play? I have Number Guessing and Rock-Paper-Scissors.")
            game_choice = take_command()
            if not game_choice: 
                talk("I couldn't hear your choice. Please say it again.")
            elif 'number guessing' in game_choice:
                number_guessing_game()
            elif 'rock paper scissors' in game_choice:
                rock_paper_scissors()
            else:
                talk("I don't know that game yet. Please choose Number Guessing or Rock-Paper-Scissors.")

           
        else:
            print("Please say the command again...")        

while True:
    run_alexa()


